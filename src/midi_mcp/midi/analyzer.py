# -*- coding: utf-8 -*-
"""
MIDI file analyzer.

Provides detailed analysis of MIDI files including structure,
content analysis, and musical pattern detection.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#

import logging
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict, Counter

try:
    import mido

    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False
    mido = None

from .exceptions import MidiError


class MidiAnalyzer:
    """
    Advanced MIDI file analyzer providing detailed musical analysis.
    """

    def __init__(self):
        """Initialize the MIDI analyzer."""
        self.logger = logging.getLogger(__name__)

        # MIDI program number to instrument name mapping (General MIDI)
        self.gm_instruments = {
            0: "Acoustic Grand Piano",
            1: "Bright Acoustic Piano",
            2: "Electric Grand Piano",
            3: "Honky-tonk Piano",
            4: "Electric Piano 1",
            5: "Electric Piano 2",
            6: "Harpsichord",
            7: "Clavi",
            8: "Celesta",
            9: "Glockenspiel",
            10: "Music Box",
            11: "Vibraphone",
            12: "Marimba",
            13: "Xylophone",
            14: "Tubular Bells",
            15: "Dulcimer",
            16: "Drawbar Organ",
            17: "Percussive Organ",
            18: "Rock Organ",
            19: "Church Organ",
            20: "Reed Organ",
            21: "Accordion",
            22: "Harmonica",
            23: "Tango Accordion",
            24: "Acoustic Guitar (nylon)",
            25: "Acoustic Guitar (steel)",
            26: "Electric Guitar (jazz)",
            27: "Electric Guitar (clean)",
            28: "Electric Guitar (muted)",
            29: "Overdriven Guitar",
            30: "Distortion Guitar",
            31: "Guitar harmonics",
            32: "Acoustic Bass",
            33: "Electric Bass (finger)",
            34: "Electric Bass (pick)",
            35: "Fretless Bass",
            36: "Slap Bass 1",
            37: "Slap Bass 2",
            38: "Synth Bass 1",
            39: "Synth Bass 2",
            40: "Violin",
            41: "Viola",
            42: "Cello",
            43: "Contrabass",
            44: "Tremolo Strings",
            45: "Pizzicato Strings",
            46: "Orchestral Harp",
            47: "Timpani",
            48: "String Ensemble 1",
            49: "String Ensemble 2",
            50: "SynthStrings 1",
            51: "SynthStrings 2",
            52: "Choir Aahs",
            53: "Voice Oohs",
            54: "Synth Voice",
            55: "Orchestra Hit",
            56: "Trumpet",
            57: "Trombone",
            58: "Tuba",
            59: "Muted Trumpet",
            60: "French Horn",
            61: "Brass Section",
            62: "SynthBrass 1",
            63: "SynthBrass 2",
            64: "Soprano Sax",
            65: "Alto Sax",
            66: "Tenor Sax",
            67: "Baritone Sax",
            68: "Oboe",
            69: "English Horn",
            70: "Bassoon",
            71: "Clarinet",
            72: "Piccolo",
            73: "Flute",
            74: "Recorder",
            75: "Pan Flute",
            76: "Blown Bottle",
            77: "Shakuhachi",
            78: "Whistle",
            79: "Ocarina",
            80: "Lead 1 (square)",
            81: "Lead 2 (sawtooth)",
            82: "Lead 3 (calliope)",
            83: "Lead 4 (chiff)",
            84: "Lead 5 (charang)",
            85: "Lead 6 (voice)",
            86: "Lead 7 (fifths)",
            87: "Lead 8 (bass + lead)",
            88: "Pad 1 (new age)",
            89: "Pad 2 (warm)",
            90: "Pad 3 (polysynth)",
            91: "Pad 4 (choir)",
            92: "Pad 5 (bowed)",
            93: "Pad 6 (metallic)",
            94: "Pad 7 (halo)",
            95: "Pad 8 (sweep)",
            96: "FX 1 (rain)",
            97: "FX 2 (soundtrack)",
            98: "FX 3 (crystal)",
            99: "FX 4 (atmosphere)",
            100: "FX 5 (brightness)",
            101: "FX 6 (goblins)",
            102: "FX 7 (echoes)",
            103: "FX 8 (sci-fi)",
            104: "Sitar",
            105: "Banjo",
            106: "Shamisen",
            107: "Koto",
            108: "Kalimba",
            109: "Bag pipe",
            110: "Fiddle",
            111: "Shanai",
            112: "Tinkle Bell",
            113: "Agogo",
            114: "Steel Drums",
            115: "Woodblock",
            116: "Taiko Drum",
            117: "Melodic Tom",
            118: "Synth Drum",
            119: "Reverse Cymbal",
            120: "Guitar Fret Noise",
            121: "Breath Noise",
            122: "Seashore",
            123: "Bird Tweet",
            124: "Telephone Ring",
            125: "Helicopter",
            126: "Applause",
            127: "Gunshot",
        }

    def analyze_comprehensive(self, midi_file) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a MIDI file.

        Args:
            midi_file: mido.MidiFile object

        Returns:
            Detailed analysis dictionary
        """
        if not MIDO_AVAILABLE:
            raise MidiError("MIDI analysis requires the 'mido' library")

        try:
            analysis = {
                "basic_info": self._analyze_basic_info(midi_file),
                "tracks": self._analyze_tracks(midi_file),
                "timing": self._analyze_timing(midi_file),
                "notes": self._analyze_notes(midi_file),
                "instruments": self._analyze_instruments(midi_file),
                "channels": self._analyze_channels(midi_file),
                "dynamics": self._analyze_dynamics(midi_file),
                "patterns": self._analyze_patterns(midi_file),
            }

            return analysis

        except Exception as e:
            self.logger.error(f"Comprehensive analysis failed: {e}")
            raise MidiError(f"Analysis failed: {str(e)}")

    def _analyze_basic_info(self, midi_file) -> Dict[str, Any]:
        """Analyze basic file information."""
        return {
            "format_type": midi_file.type,
            "tracks": len(midi_file.tracks),
            "ticks_per_beat": midi_file.ticks_per_beat,
            "duration_seconds": midi_file.length,
            "total_messages": sum(len(track) for track in midi_file.tracks),
            "file_size_estimate": sum(len(str(msg)) for track in midi_file.tracks for msg in track),
        }

    def _analyze_tracks(self, midi_file) -> List[Dict[str, Any]]:
        """Analyze individual tracks."""
        tracks_analysis = []

        for i, track in enumerate(midi_file.tracks):
            track_info = {
                "index": i,
                "name": None,
                "messages": len(track),
                "note_events": 0,
                "control_events": 0,
                "program_changes": 0,
                "meta_messages": 0,
                "channels_used": set(),
                "duration": 0.0,
            }

            current_time = 0.0
            for msg in track:
                current_time += msg.time

                if hasattr(msg, "type"):
                    if msg.type == "track_name":
                        track_info["name"] = msg.name
                    elif msg.type in ["note_on", "note_off"]:
                        track_info["note_events"] += 1
                        track_info["channels_used"].add(msg.channel)
                    elif msg.type == "control_change":
                        track_info["control_events"] += 1
                        track_info["channels_used"].add(msg.channel)
                    elif msg.type == "program_change":
                        track_info["program_changes"] += 1
                        track_info["channels_used"].add(msg.channel)
                    elif hasattr(msg, "is_meta") and msg.is_meta:
                        track_info["meta_messages"] += 1

            track_info["duration"] = current_time
            track_info["channels_used"] = list(track_info["channels_used"])

            if track_info["name"] is None:
                track_info["name"] = f"Track {i}"

            tracks_analysis.append(track_info)

        return tracks_analysis

    def _analyze_timing(self, midi_file) -> Dict[str, Any]:
        """Analyze timing and tempo information."""
        tempo_changes = []
        time_signatures = []
        current_time = 0.0

        for track in midi_file.tracks:
            track_time = 0.0
            for msg in track:
                track_time += msg.time

                if hasattr(msg, "type"):
                    if msg.type == "set_tempo":
                        tempo_bpm = round(mido.tempo2bpm(msg.tempo))
                        tempo_changes.append(
                            {"time": track_time, "tempo_bpm": tempo_bpm, "tempo_microseconds": msg.tempo}
                        )
                    elif msg.type == "time_signature":
                        time_signatures.append(
                            {
                                "time": track_time,
                                "numerator": msg.numerator,
                                "denominator": msg.denominator,
                                "clocks_per_click": msg.clocks_per_click,
                                "notated_32nd_notes_per_beat": msg.notated_32nd_notes_per_beat,
                            }
                        )

        # Default values if no tempo/time signature found
        if not tempo_changes:
            tempo_changes.append({"time": 0.0, "tempo_bpm": 120, "tempo_microseconds": 500000})

        if not time_signatures:
            time_signatures.append(
                {
                    "time": 0.0,
                    "numerator": 4,
                    "denominator": 4,
                    "clocks_per_click": 24,
                    "notated_32nd_notes_per_beat": 8,
                }
            )

        return {
            "tempo_changes": tempo_changes,
            "time_signatures": time_signatures,
            "initial_tempo": tempo_changes[0]["tempo_bpm"],
            "initial_time_signature": (time_signatures[0]["numerator"], time_signatures[0]["denominator"]),
            "tempo_stable": len(tempo_changes) <= 1,
            "time_signature_stable": len(time_signatures) <= 1,
        }

    def _analyze_notes(self, midi_file) -> Dict[str, Any]:
        """Analyze note information."""
        notes = []
        note_on_times = {}  # Track note on times for duration calculation

        for track_idx, track in enumerate(midi_file.tracks):
            current_time = 0.0

            for msg in track:
                current_time += msg.time

                if hasattr(msg, "type"):
                    if msg.type == "note_on" and msg.velocity > 0:
                        note_key = (track_idx, msg.channel, msg.note)
                        note_on_times[note_key] = current_time
                    elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                        note_key = (track_idx, msg.channel, msg.note)
                        if note_key in note_on_times:
                            start_time = note_on_times[note_key]
                            duration = current_time - start_time

                            notes.append(
                                {
                                    "track": track_idx,
                                    "channel": msg.channel,
                                    "note": msg.note,
                                    "velocity": getattr(msg, "velocity", 64),
                                    "start_time": start_time,
                                    "duration": duration,
                                    "end_time": current_time,
                                }
                            )

                            del note_on_times[note_key]

        if not notes:
            return {
                "total_notes": 0,
                "note_range": {"min": 0, "max": 0},
                "average_duration": 0,
                "average_velocity": 0,
                "note_density": 0,
                "pitch_histogram": {},
                "velocity_histogram": {},
            }

        # Calculate statistics
        note_numbers = [note["note"] for note in notes]
        velocities = [note["velocity"] for note in notes]
        durations = [note["duration"] for note in notes]

        return {
            "total_notes": len(notes),
            "note_range": {"min": min(note_numbers), "max": max(note_numbers)},
            "average_duration": sum(durations) / len(durations),
            "average_velocity": sum(velocities) / len(velocities),
            "note_density": len(notes) / midi_file.length if midi_file.length > 0 else 0,
            "pitch_histogram": dict(Counter(note_numbers)),
            "velocity_histogram": dict(Counter(velocities)),
            "notes": notes[:100],  # Limit to first 100 notes for performance
        }

    def _analyze_instruments(self, midi_file) -> Dict[str, Any]:
        """Analyze instrument usage."""
        programs_per_channel = defaultdict(set)
        program_changes = []

        for track_idx, track in enumerate(midi_file.tracks):
            current_time = 0.0

            for msg in track:
                current_time += msg.time

                if hasattr(msg, "type") and msg.type == "program_change":
                    programs_per_channel[msg.channel].add(msg.program)
                    program_changes.append(
                        {
                            "track": track_idx,
                            "channel": msg.channel,
                            "program": msg.program,
                            "instrument": self.gm_instruments.get(msg.program, f"Unknown ({msg.program})"),
                            "time": current_time,
                        }
                    )

        # Convert sets to lists for JSON serialization
        instruments_by_channel = {}
        for channel, programs in programs_per_channel.items():
            instruments_by_channel[channel] = [
                {"program": program, "instrument": self.gm_instruments.get(program, f"Unknown ({program})")}
                for program in sorted(programs)
            ]

        unique_instruments = set()
        for programs in programs_per_channel.values():
            unique_instruments.update(programs)

        return {
            "unique_instruments": len(unique_instruments),
            "instruments_by_channel": instruments_by_channel,
            "program_changes": program_changes,
            "instrument_list": [
                self.gm_instruments.get(program, f"Unknown ({program})") for program in sorted(unique_instruments)
            ],
        }

    def _analyze_channels(self, midi_file) -> Dict[str, Any]:
        """Analyze MIDI channel usage."""
        channel_usage = defaultdict(
            lambda: {
                "note_events": 0,
                "control_events": 0,
                "program_changes": 0,
                "notes": [],
                "controllers_used": set(),
            }
        )

        for track in midi_file.tracks:
            for msg in track:
                if hasattr(msg, "channel"):
                    channel = msg.channel

                    if hasattr(msg, "type"):
                        if msg.type in ["note_on", "note_off"]:
                            channel_usage[channel]["note_events"] += 1
                            if msg.type == "note_on" and msg.velocity > 0:
                                channel_usage[channel]["notes"].append(msg.note)
                        elif msg.type == "control_change":
                            channel_usage[channel]["control_events"] += 1
                            channel_usage[channel]["controllers_used"].add(msg.control)
                        elif msg.type == "program_change":
                            channel_usage[channel]["program_changes"] += 1

        # Convert to serializable format
        channels_summary = {}
        for channel, data in channel_usage.items():
            channels_summary[channel] = {
                "note_events": data["note_events"],
                "control_events": data["control_events"],
                "program_changes": data["program_changes"],
                "unique_notes": len(set(data["notes"])),
                "note_range": {
                    "min": min(data["notes"]) if data["notes"] else 0,
                    "max": max(data["notes"]) if data["notes"] else 0,
                },
                "controllers_used": list(data["controllers_used"]),
                "is_drum_channel": channel == 9,  # Channel 10 (0-indexed 9) is drums in GM
            }

        return {
            "channels_used": list(channel_usage.keys()),
            "total_channels": len(channel_usage),
            "channel_summary": channels_summary,
        }

    def _analyze_dynamics(self, midi_file) -> Dict[str, Any]:
        """Analyze velocity and dynamic information."""
        velocities = []
        velocity_changes = []

        for track in midi_file.tracks:
            current_time = 0.0

            for msg in track:
                current_time += msg.time

                if hasattr(msg, "type") and msg.type == "note_on" and msg.velocity > 0:
                    velocities.append(msg.velocity)
                    velocity_changes.append(
                        {"time": current_time, "velocity": msg.velocity, "note": msg.note, "channel": msg.channel}
                    )

        if not velocities:
            return {
                "velocity_range": {"min": 0, "max": 0},
                "average_velocity": 0,
                "velocity_variation": 0,
                "dynamic_range": "No notes found",
            }

        velocity_min = min(velocities)
        velocity_max = max(velocities)
        velocity_avg = sum(velocities) / len(velocities)
        velocity_std = (sum((v - velocity_avg) ** 2 for v in velocities) / len(velocities)) ** 0.5

        # Classify dynamic range
        if velocity_max - velocity_min < 20:
            dynamic_range = "Very Limited"
        elif velocity_max - velocity_min < 40:
            dynamic_range = "Limited"
        elif velocity_max - velocity_min < 60:
            dynamic_range = "Moderate"
        elif velocity_max - velocity_min < 80:
            dynamic_range = "Wide"
        else:
            dynamic_range = "Very Wide"

        return {
            "velocity_range": {"min": velocity_min, "max": velocity_max},
            "average_velocity": round(velocity_avg, 2),
            "velocity_variation": round(velocity_std, 2),
            "dynamic_range": dynamic_range,
            "velocity_histogram": dict(Counter(velocities)),
        }

    def _analyze_patterns(self, midi_file) -> Dict[str, Any]:
        """Analyze musical patterns and structure."""
        # This is a basic pattern analysis for Phase 2
        # More sophisticated pattern detection can be added in later phases

        track_lengths = []
        message_types = Counter()

        for track in midi_file.tracks:
            track_length = sum(msg.time for msg in track)
            track_lengths.append(track_length)

            for msg in track:
                if hasattr(msg, "type"):
                    message_types[msg.type] += 1

        return {
            "track_length_variation": {
                "min": min(track_lengths) if track_lengths else 0,
                "max": max(track_lengths) if track_lengths else 0,
                "average": sum(track_lengths) / len(track_lengths) if track_lengths else 0,
            },
            "message_type_distribution": dict(message_types),
            "structural_analysis": "Basic pattern analysis - more sophisticated analysis available in later phases",
        }
