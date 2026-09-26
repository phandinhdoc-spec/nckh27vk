import AVFoundation
import CoreMedia
import Foundation
import Speech

enum DictationTestError: LocalizedError {
    case missingArgument
    case fileNotFound(String)
    case unsupportedVietnameseLocale
    case unavailableSpeechFormat
    case converterCreationFailed
    case bufferCreationFailed
    case audioConversionFailed(String)
    case emptyAudio
    case emptyTranscript

    var errorDescription: String? {
        switch self {
        case .missingArgument:
            return """
            Chưa cung cấp file âm thanh.

            Cách dùng:
              ./DictationTest record.wav
              ./DictationTest record.m4a
            """

        case .fileNotFound(let path):
            return "File không tồn tại: \(path)"

        case .unsupportedVietnameseLocale:
            return "DictationTranscriber không hỗ trợ locale vi_VN."

        case .unavailableSpeechFormat:
            return "Không xác định được định dạng âm thanh tương thích với DictationTranscriber."

        case .converterCreationFailed:
            return "Không thể tạo AVAudioConverter."

        case .bufferCreationFailed:
            return "Không thể tạo buffer âm thanh."

        case .audioConversionFailed(let message):
            return "Chuyển đổi âm thanh thất bại: \(message)"

        case .emptyAudio:
            return "File âm thanh không chứa mẫu dữ liệu."

        case .emptyTranscript:
            return "Không nhận dạng được nội dung giọng nói."
        }
    }
}

struct PreparedAudioFile {
    let url: URL
    let isTemporary: Bool
}

@main
struct DictationTest {
    static func main() async {
        do {
            let sourceURL = try getSourceURL()
            let sourceFile = try AVAudioFile(forReading: sourceURL)
            let sourceFormat = sourceFile.processingFormat

            let requestedLocale = Locale(identifier: "vi_VN")

            guard let locale =
                await DictationTranscriber.supportedLocale(
                    equivalentTo: requestedLocale
                )
            else {
                throw DictationTestError.unsupportedVietnameseLocale
            }

            let transcriber = DictationTranscriber(
                locale: locale,
                preset: .longDictation
            )

            guard let targetFormat =
                await SpeechAnalyzer.bestAvailableAudioFormat(
                    compatibleWith: [transcriber],
                    considering: sourceFormat
                )
            else {
                throw DictationTestError.unavailableSpeechFormat
            }

            printSourceInformation(
                url: sourceURL,
                file: sourceFile
            )

            printFormat(
                title: "Định dạng Speech yêu cầu",
                format: targetFormat
            )

            print("Locale sử dụng: \(locale.identifier)")

            let preparedFile = try prepareAudioFile(
                sourceURL: sourceURL,
                targetFormat: targetFormat
            )

            defer {
                if preparedFile.isTemporary {
                    try? FileManager.default.removeItem(
                        at: preparedFile.url
                    )
                }
            }

            if preparedFile.isTemporary {
                print("Trạng thái: đã chuyển đổi sang định dạng Speech.")
            } else {
                print("Trạng thái: file nguồn đã tương thích.")
            }

            print("\n--- Bắt đầu nhận dạng ---")

            let clock = ContinuousClock()
            let startTime = clock.now

            let transcript = try await transcribe(
                audioURL: preparedFile.url,
                transcriber: transcriber
            )

            let elapsed = startTime.duration(to: clock.now)

            print("\n--- Kết quả cuối cùng ---")
            print(transcript)
            print(
                String(
                    format: "\nThời gian xử lý: %.3f giây",
                    durationInSeconds(elapsed)
                )
            )
        } catch {
            let message =
                (error as? LocalizedError)?.errorDescription
                ?? error.localizedDescription

            FileHandle.standardError.write(
                Data("Lỗi: \(message)\n".utf8)
            )

            Foundation.exit(EXIT_FAILURE)
        }
    }

    private static func transcribe(
        audioURL: URL,
        transcriber: DictationTranscriber
    ) async throws -> String {
        let analyzer = SpeechAnalyzer(
            modules: [transcriber]
        )

        let resultTask = Task<String, Error> {
            var transcriptParts: [String] = []

            for try await result in transcriber.results {
                let text = String(result.text.characters)
                    .trimmingCharacters(
                        in: .whitespacesAndNewlines
                    )

                guard !text.isEmpty else {
                    continue
                }

                print("Đang nhận dạng: \(text)")
                transcriptParts.append(text)
            }

            return mergeTranscriptParts(transcriptParts)
        }

        do {
            let audioFile = try AVAudioFile(
                forReading: audioURL
            )

            guard let lastSampleTime =
                try await analyzer.analyzeSequence(
                    from: audioFile
                )
            else {
                resultTask.cancel()
                await analyzer.cancelAndFinishNow()
                throw DictationTestError.emptyAudio
            }

            try await analyzer.finalizeAndFinish(
                through: lastSampleTime
            )

            let transcript = try await resultTask.value
                .trimmingCharacters(
                    in: .whitespacesAndNewlines
                )

            guard !transcript.isEmpty else {
                throw DictationTestError.emptyTranscript
            }

            return transcript
        } catch {
            resultTask.cancel()
            await analyzer.cancelAndFinishNow()
            throw error
        }
    }

    private static func mergeTranscriptParts(
        _ parts: [String]
    ) -> String {
        guard let first = parts.first else {
            return ""
        }

        var merged = first

        for part in parts.dropFirst() {
            if part.hasPrefix(merged) {
                merged = part
            } else if merged.hasPrefix(part) {
                continue
            } else {
                merged += " " + part
            }
        }

        return merged
    }

    private static func prepareAudioFile(
        sourceURL: URL,
        targetFormat: AVAudioFormat
    ) throws -> PreparedAudioFile {
        let sourceFile = try AVAudioFile(
            forReading: sourceURL
        )

        let sourceFormat = sourceFile.processingFormat

        if formatsAreEquivalent(
            sourceFormat,
            targetFormat
        ) {
            return PreparedAudioFile(
                url: sourceURL,
                isTemporary: false
            )
        }

        let temporaryURL = FileManager.default
            .temporaryDirectory
            .appendingPathComponent(
                "dictation-\(UUID().uuidString)"
            )
            .appendingPathExtension("caf")

        do {
            try convertAudio(
                sourceFile: sourceFile,
                destinationURL: temporaryURL,
                sourceFormat: sourceFormat,
                targetFormat: targetFormat
            )

            return PreparedAudioFile(
                url: temporaryURL,
                isTemporary: true
            )
        } catch {
            try? FileManager.default.removeItem(
                at: temporaryURL
            )

            throw error
        }
    }

    private static func convertAudio(
        sourceFile: AVAudioFile,
        destinationURL: URL,
        sourceFormat: AVAudioFormat,
        targetFormat: AVAudioFormat
    ) throws {
        guard let converter = AVAudioConverter(
            from: sourceFormat,
            to: targetFormat
        ) else {
            throw DictationTestError.converterCreationFailed
        }

        let destinationFile = try AVAudioFile(
            forWriting: destinationURL,
            settings: targetFormat.settings,
            commonFormat: targetFormat.commonFormat,
            interleaved: targetFormat.isInterleaved
        )

        let inputCapacity: AVAudioFrameCount = 4096

        guard let inputBuffer = AVAudioPCMBuffer(
            pcmFormat: sourceFormat,
            frameCapacity: inputCapacity
        ) else {
            throw DictationTestError.bufferCreationFailed
        }

        let sampleRateRatio =
            targetFormat.sampleRate
            / sourceFormat.sampleRate

        let estimatedOutputCapacity =
            ceil(Double(inputCapacity) * sampleRateRatio) + 64

        let outputCapacity = AVAudioFrameCount(
            max(4096, estimatedOutputCapacity)
        )

        guard let outputBuffer = AVAudioPCMBuffer(
            pcmFormat: targetFormat,
            frameCapacity: outputCapacity
        ) else {
            throw DictationTestError.bufferCreationFailed
        }

        var reachedEndOfInput = false
        var sourceReadError: Error?

        conversionLoop: while true {
            outputBuffer.frameLength = 0

            var conversionError: NSError?

            let status = converter.convert(
                to: outputBuffer,
                error: &conversionError
            ) { requestedPackets, inputStatus in
                if reachedEndOfInput {
                    inputStatus.pointee = .endOfStream
                    return nil
                }

                do {
                    inputBuffer.frameLength = 0

                    let remainingFrames =
                        sourceFile.length - sourceFile.framePosition

                    guard remainingFrames > 0 else {
                        reachedEndOfInput = true
                        inputStatus.pointee = .endOfStream
                        return nil
                    }

                    let requestedFrames = AVAudioFrameCount(
                        requestedPackets
                    )

                    let safeRemainingFrames = AVAudioFrameCount(
                        min(
                            remainingFrames,
                            AVAudioFramePosition(
                                AVAudioFrameCount.max
                            )
                        )
                    )

                    let framesToRead = min(
                        requestedFrames,
                        inputBuffer.frameCapacity,
                        safeRemainingFrames
                    )

                    try sourceFile.read(
                        into: inputBuffer,
                        frameCount: framesToRead
                    )

                    if inputBuffer.frameLength == 0
                        || sourceFile.framePosition >= sourceFile.length
                    {
                        if inputBuffer.frameLength == 0 {
                            reachedEndOfInput = true
                            inputStatus.pointee = .endOfStream
                            return nil
                        }
                    }

                    inputStatus.pointee = .haveData
                    return inputBuffer
                } catch {
                    /*
                     AVAudioFile có thể báo EOF bằng OSStatus -39.
                     Nếu con trỏ đã ở cuối file thì đây là kết thúc
                     bình thường, không phải lỗi dữ liệu.
                    */
                    if sourceFile.framePosition >= sourceFile.length {
                        reachedEndOfInput = true
                        inputStatus.pointee = .endOfStream
                        return nil
                    }

                    sourceReadError = error
                    reachedEndOfInput = true
                    inputStatus.pointee = .endOfStream
                    return nil
                }
            }

            if let sourceReadError {
                throw DictationTestError.audioConversionFailed(
                    "Không đọc được file nguồn: "
                    + sourceReadError.localizedDescription
                )
            }

            if outputBuffer.frameLength > 0 {
                try destinationFile.write(
                    from: outputBuffer
                )
            }

            switch status {
            case .haveData:
                continue conversionLoop

            case .inputRanDry:
                continue conversionLoop

            case .endOfStream:
                break conversionLoop

            case .error:
                throw DictationTestError.audioConversionFailed(
                    conversionError?.localizedDescription
                    ?? "AVAudioConverter trả về trạng thái lỗi."
                )

            @unknown default:
                throw DictationTestError.audioConversionFailed(
                    "AVAudioConverter trả về trạng thái không xác định."
                )
            }
        }
    }

    private static func formatsAreEquivalent(
        _ first: AVAudioFormat,
        _ second: AVAudioFormat
    ) -> Bool {
        let sampleRateDifference = abs(
            first.sampleRate - second.sampleRate
        )

        return sampleRateDifference < 0.5
            && first.channelCount == second.channelCount
            && first.commonFormat == second.commonFormat
            && first.isInterleaved == second.isInterleaved
    }

    private static func getSourceURL() throws -> URL {
        let arguments = CommandLine.arguments

        guard arguments.count >= 2 else {
            throw DictationTestError.missingArgument
        }

        let expandedPath = NSString(
            string: arguments[1]
        ).expandingTildeInPath

        let absolutePath: String

        if expandedPath.hasPrefix("/") {
            absolutePath = expandedPath
        } else {
            absolutePath = URL(
                fileURLWithPath: FileManager.default.currentDirectoryPath
            )
            .appendingPathComponent(expandedPath)
            .standardizedFileURL
            .path
        }

        guard FileManager.default.fileExists(
            atPath: absolutePath
        ) else {
            throw DictationTestError.fileNotFound(
                absolutePath
            )
        }

        return URL(
            fileURLWithPath: absolutePath
        )
    }

    private static func printSourceInformation(
        url: URL,
        file: AVAudioFile
    ) {
        let format = file.processingFormat

        let duration =
            format.sampleRate > 0
            ? Double(file.length) / format.sampleRate
            : 0

        print("--- Thông tin file nguồn ---")
        print("Đường dẫn: \(url.path)")

        printFormat(
            title: "Định dạng file",
            format: format
        )

        print(
            String(
                format: "Thời lượng: %.2f giây",
                duration
            )
        )
    }

    private static func printFormat(
        title: String,
        format: AVAudioFormat
    ) {
        let layout =
            format.isInterleaved
            ? "interleaved"
            : "non-interleaved"

        print(
            "\(title): "
            + "\(Int(format.sampleRate)) Hz, "
            + "\(format.channelCount) kênh, "
            + "\(format.commonFormat), "
            + layout
        )
    }

    private static func durationInSeconds(
        _ duration: Duration
    ) -> Double {
        let components = duration.components

        return Double(components.seconds)
            + Double(components.attoseconds) / 1e18
    }
}
