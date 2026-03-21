#include <Arduino.h>

// ─── Pin Assignment ──────────────────────────────────────────────
constexpr int TONE_PIN = 24;

// ─── RTTTL Note Frequency Table ─────────────────────────────────
// Index 0 = rest, then C4..B4, C5..B5, C6..B6, C7..B7
// Each octave has 12 semitones: C, C#, D, D#, E, F, F#, G, G#, A, A#, B

#define OCTAVE_OFFSET 0

const int notes[] = { 0,
  262, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494,   // octave 4
  523, 554, 587, 622, 659, 698, 740, 784, 831, 880, 932, 988,   // octave 5
  1047, 1109, 1175, 1245, 1319, 1397, 1480, 1568, 1661, 1760, 1865, 1976, // octave 6
  2093, 2217, 2349, 2489, 2637, 2794, 2960, 3136, 3322, 3520, 3729, 3951  // octave 7
};

// ─── RTTTL Songs ─────────────────────────────────────────────────
// Uncomment one song at a time to play it.
// Format: name:d=<default_duration>,o=<default_octave>,b=<bpm>:<notes>

const char* song = "NeverGonna:d=4,o=5,b=200:8g,8a,8c6,8a,e6,8p,e6,8p,d6.,p,8p,8g,8a,8c6,8a,d6,8p,d6,8p,c6,8b,a.,8g,8a,8c6,8a,2c6,d6,b,a,g.,8p,g,2d6,2c6.";
//const char* song = "StarWars:d=4,o=5,b=45:32p,32f#,32f#,32f#,8b.,8f#.6,32e6,32d#6,32c#6,8b.6,16f#.6,32e6,32d#6,32c#6,8b.6,16f#.6,32e6,32d#6,32e6,8c#.6";
//const char* song = "MissionImp:d=16,o=6,b=95:32d,32d#,32d,32d#,32d,32d#,32d,32d#,32d,32d,32d#,32e,32f,32f#,32g,g,8p,g,8p,a#,p,c7,p,g,8p,g,8p,f,p,f#,p,g,8p,g,8p,a#,p,c7,p,g,8p,g,8p,f,p,f#,p,a#,g,2d,32p,a#,g,2c#,32p,a#,g,2c,a#5,8c,2p,32p,a#5,g5,2f#,32p,a#5,g5,2f,32p,a#5,g5,2e,d#,8d";
//const char* song = "Indiana:d=4,o=5,b=250:e,8p,8f,8g,8p,1c6,8p.,d,8p,8e,1f,p.,g,8p,8a,8b,8p,1f6,p,a,8p,8b,2c6,2d6,2e6";
//const char* song = "Simpsons:d=4,o=5,b=160:c.6,e6,f#6,8a6,g.6,e6,c6,8a,8f#,8f#,8f#,2g";
//const char* song = "TakeOnMe:d=4,o=4,b=160:8f#5,8f#5,8f#5,8d5,8p,8b,8p,8e5,8p,8e5,8p,8e5,8g#5,8g#5,8a5,8b5,8a5,8a5,8a5,8e5,8p,8d5,8p,8f#5,8p,8f#5,8p,8f#5,8e5,8e5,8f#5,8e5";
//const char* song = "Jeopardy:d=4,o=6,b=125:c,f,c,f5,c,f,2c,c,f,c,f,a.,8g,8f,8e,8d,8c#,c,f,c,f5,c,f,2c,f.,8d,c,a#5,a5,g5,f5,p,d#,g#,d#,g#5,d#,g#,2d#,d#,g#,d#,g#,c.7,8a#,8g#,8g,8f,8e,d#,g#,d#,g#5,d#,g#,2d#,g#.,8f,d#,c#,c,p,a#5,p,g#5";
//const char* song = "Flinstones:d=4,o=5,b=200:g#,c#,8p,c#6,8a#,g#,c#,8p,g#,8f#,8f,8f,8f#,8g#,c#,d#,2f,2p,g#,c#,8p,c#6,8a#,g#,c#,8p,g#,8f#,8f,8f,8f#,8g#,c#,d#,2c#";
//const char* song = "MASH:d=8,o=5,b=140:4a,4g,f#,g,p,f#,p,e,p,4d,p,f#,p,a,p,4b,2p,4a,4g,f#,g,p,f#,p,e,p,4d,p,f#,p,a,p,4b,2p";

// ─── Forward Declarations ────────────────────────────────────────
void play_rtttl(const char* p);

// ─── Setup & Loop ────────────────────────────────────────────────

void setup() {
  Serial.begin(9600);
  Serial.println("RTTTL Melody Player");
  Serial.println("Playing...");
  play_rtttl(song);
  Serial.println("Done!");
}

void loop() {
  // Song plays once in setup, then stops.
}

// ─── RTTTL Parser ────────────────────────────────────────────────

void play_rtttl(const char* p) {
  // Skip the name (everything before the first colon)
  while (*p != ':') {
    if (*p == '\0') return;
    p++;
  }
  p++;  // skip ':'

  // Parse default values: d=<duration>, o=<octave>, b=<bpm>
  int default_dur = 4;
  int default_oct = 6;
  int bpm = 63;

  // Parse d=N
  if (*p == 'd') {
    p++; p++;  // skip 'd='
    default_dur = 0;
    while (isdigit(*p)) {
      default_dur = default_dur * 10 + (*p - '0');
      p++;
    }
    if (*p == ',') p++;  // skip comma
  }

  // Parse o=N
  if (*p == 'o') {
    p++; p++;  // skip 'o='
    default_oct = *p - '0';
    p++;
    if (*p == ',') p++;  // skip comma
  }

  // Parse b=N
  if (*p == 'b') {
    p++; p++;  // skip 'b='
    bpm = 0;
    while (isdigit(*p)) {
      bpm = bpm * 10 + (*p - '0');
      p++;
    }
    if (*p == ':') p++;  // skip colon before notes
  }

  // BPM is based on quarter notes — calculate whole note duration in ms
  long wholenote = (60 * 1000L / bpm) * 4;

  Serial.print("  BPM: ");
  Serial.print(bpm);
  Serial.print("  Default duration: ");
  Serial.print(default_dur);
  Serial.print("  Default octave: ");
  Serial.println(default_oct);

  // Parse and play each note
  while (*p) {
    // Skip whitespace and commas
    while (*p == ',' || *p == ' ') p++;
    if (*p == '\0') break;

    // 1. Parse optional duration prefix (e.g. "8" in "8g")
    int duration = 0;
    while (isdigit(*p)) {
      duration = duration * 10 + (*p - '0');
      p++;
    }
    if (duration == 0) duration = default_dur;

    // 2. Parse the note letter (c, d, e, f, g, a, b, p=pause)
    int note = 0;
    switch (tolower(*p)) {
      case 'c': note = 1;  break;
      case 'd': note = 3;  break;
      case 'e': note = 5;  break;
      case 'f': note = 6;  break;
      case 'g': note = 8;  break;
      case 'a': note = 10; break;
      case 'b': note = 12; break;
      case 'p': note = 0;  break;
      default:  note = 0;  break;
    }
    p++;

    // 3. Check for sharp (#)
    if (*p == '#') {
      note++;
      p++;
    }

    // 4. Check for dotted note (adds 50% duration)
    bool dotted = false;
    if (*p == '.') {
      dotted = true;
      p++;
    }

    // 5. Parse optional octave override
    int octave = default_oct;
    if (isdigit(*p)) {
      octave = *p - '0';
      p++;
    }

    // 6. Check for dotted note after octave (some RTTTL strings put it here)
    if (*p == '.') {
      dotted = true;
      p++;
    }

    // Calculate duration in milliseconds
    long note_duration;
    if (duration > 0) {
      note_duration = wholenote / duration;
    } else {
      note_duration = wholenote / default_dur;
    }
    if (dotted) {
      note_duration += note_duration / 2;  // dotted = 150% length
    }

    // Play the note or rest
    if (note) {
      int freq_index = (octave - 4) * 12 + note + OCTAVE_OFFSET;
      if (freq_index >= 1 && freq_index <= 48) {
        tone(TONE_PIN, notes[freq_index]);
      }
      delay(note_duration);
      noTone(TONE_PIN);
    } else {
      // Rest — silence for the duration
      delay(note_duration);
    }

    // Brief pause between notes for articulation
    delay(20);
  }

  noTone(TONE_PIN);
}
