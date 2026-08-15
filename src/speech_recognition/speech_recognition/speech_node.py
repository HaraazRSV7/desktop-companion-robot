#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import sounddevice as sd
import soundfile as sf

from faster_whisper import WhisperModel


class SpeechRecognitionNode(Node):

    def __init__(self):
        super().__init__("speech_recognition_node")

        # Publisher
        self.publisher_ = self.create_publisher(
            String,
            "/speech_text",
            10
        )

        # Load Whisper model only once
        self.get_logger().info("Loading Whisper model...")


        self.model = WhisperModel(
            "base",
            device="cuda",
            compute_type="float16"
        )


        self.get_logger().info("Whisper model loaded successfully!")

        # Record speech every 5 seconds
        self.timer = self.create_timer(
            5.0,
            self.listen_callback
        )

    def listen_callback(self):

        samplerate = 16000
        duration = 4

        self.get_logger().info("Listening...")

        audio = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        # Save recorded audio
        sf.write("audio.wav", audio, samplerate)

        self.get_logger().info("Transcribing...")

        segments, info = self.model.transcribe(
            "audio.wav",
            beam_size=2,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        text = ""

        for segment in segments:
            text += segment.text + " "

        text = text.strip()

        self.get_logger().info(f"Recognized: {text}")

        msg = String()
        msg.data = text

        self.publisher_.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = SpeechRecognitionNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()