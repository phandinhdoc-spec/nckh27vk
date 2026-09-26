import Foundation
import FoundationModels
import Hummingbird
import ImageIO
import NIOCore

struct ClassificationResponse: ResponseCodable {
    let code: String
}

enum WasteCode: String, CaseIterable {
    case organic = "RHC"
    case inorganic = "RVC"
    case sharp = "RNH"
    case chemical = "RKH"
    case other = "RK"
}

enum WasteClassifier {
    static let model = SystemLanguageModel.default

    static var availability: String {
        switch model.availability {
        case .available: "available"
        case .unavailable(.deviceNotEligible): "device_not_eligible"
        case .unavailable(.appleIntelligenceNotEnabled): "apple_intelligence_not_enabled"
        case .unavailable(.modelNotReady): "model_not_ready"
        case .unavailable: "unavailable"
        }
    }

    static func normalize(_ output: String) -> WasteCode {
        let tokens = output.uppercased().split { !$0.isLetter }
        let matches = Set(tokens.compactMap { WasteCode(rawValue: String($0)) })
        return matches.count == 1 ? matches.first! : .other
    }

    static func classify(_ data: Data) async throws -> WasteCode {
        guard case .available = model.availability,
              let source = CGImageSourceCreateWithData(data as CFData, nil),
              let image = CGImageSourceCreateImageAtIndex(source, 0, nil)
        else { return .other }

        let session = LanguageModelSession(
            model: model,
            instructions: """
            Bạn là bộ phân loại rác hỗ trợ người khiếm thị. Chỉ trả về đúng một mã: RHC, RVC, RNH, RKH hoặc RK. Không giải thích, không thêm dấu câu. Nếu ảnh mờ, có nhiều vật thể chính hoặc không chắc chắn, trả RK. Vì an toàn, ưu tiên nhận diện RKH trước RNH, rồi mới RHC hoặc RVC.
            """
        )
        let response = try await session.respond {
            """
            Phân loại vật thể chính trong ảnh theo đúng quy tắc:
            RKH: vật hoặc bao bì có ký hiệu hóa chất độc hại, ăn mòn, dễ cháy hoặc chất độc.
            RNH: kim tiêm, kim, dao, lưỡi lam, đinh, mảnh kính vỡ hoặc vật sắc nhọn nguy hiểm.
            RHC: thức ăn thừa, rau, củ, quả, vỏ trái cây, lá cây hoặc chất hữu cơ dễ phân hủy.
            RVC: chai nhựa, lon, kim loại, giấy, bìa, thủy tinh nguyên vẹn hoặc rác vô cơ thông thường.
            RK: loại khác, ảnh không rõ hoặc không chắc chắn.
            Chỉ trả một mã.
            """
            Attachment(image)
        }
        return normalize(response.content)
    }
}

@main
enum GreenEyeServer {
    static func main() async throws {
        if CommandLine.arguments.contains("--self-test") {
            precondition(WasteClassifier.normalize("RHC") == .organic)
            precondition(WasteClassifier.normalize("`RKH`") == .chemical)
            precondition(WasteClassifier.normalize("RHC RVC") == .other)
            precondition(WasteClassifier.normalize("không rõ") == .other)
            print("self-test: ok; Apple Intelligence: \(WasteClassifier.availability)")
            return
        }

        let host = ProcessInfo.processInfo.environment["GREEN_EYE_HOST"] ?? "0.0.0.0"
        let port = Int(ProcessInfo.processInfo.environment["GREEN_EYE_PORT"] ?? "8765") ?? 8765
        let router = Router()

        router.get("/health") { _, _ in "ok; apple_intelligence=\(WasteClassifier.availability)" }
        router.post("/classify") { request, _ -> ClassificationResponse in
            let buffer = try await request.body.collect(upTo: 5 * 1_024 * 1_024)
            guard buffer.readableBytes > 0 else { return .init(code: WasteCode.other.rawValue) }
            do {
                let code = try await WasteClassifier.classify(Data(buffer.readableBytesView))
                return .init(code: code.rawValue)
            } catch {
                return .init(code: WasteCode.other.rawValue)
            }
        }

        print("GreenEyeServer: http://\(host):\(port)")
        try await Application(
            router: router,
            configuration: .init(address: .hostname(host, port: port))
        ).runService()
    }
}
