import package.compose as compose
import pretty_midi

input_path = 'pitches/七第兄甚'
filename = '/Users/apple/Git_repo/Xian_Drum_Music/Composed/七第兄甚/七第兄甚吴字调.mid'
output_path = '/Users/apple/Git_repo/Xian_Drum_Music/Composed/七第兄甚/'
note_num = 15

if __name__ == '__main__':
    _, _, pauses = compose.cutpitches_pitchesrepeated(input_path, note_num)
    pauses = pauses[0]
    pitchset = []
    timeset = []

    midi_data = pretty_midi.PrettyMIDI(filename)
    last_pitch = midi_data.instruments[0].notes[0].pitch
    pitch_cnt = 0
    pauses_record = []
    for instrument in midi_data.instruments:
        if not instrument.is_drum:
            for note in instrument.notes:
                if abs(note.pitch - last_pitch) > 4:
                    if (pitch_cnt - 1 + 1) in pauses:
                        pauses_record.append(pitch_cnt - 1 + 1)
                pitchset.append(note.pitch)
                timeset.append(round(note.end - note.start, 1))
                pitch_cnt += 1
                last_pitch = note.pitch
    print(pauses_record)

    timecnt = 0
    lastend = 0
    cello_c_chord = pretty_midi.PrettyMIDI()
    cello_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    cello = pretty_midi.Instrument(program=cello_program)
    for i in range(len(pitchset)):
        note = pretty_midi.Note(velocity=80  , pitch=pitchset[i], start=lastend, end=lastend + timeset[i])
        cello.notes.append(note)
        lastend = lastend + timeset[i]
        timecnt = timecnt + timeset[i]
        if (i+1) in pauses_record:
            bartime_rest = 2.4 * (int((timecnt) / 2.4) + 1) - timecnt
            lastend = lastend + bartime_rest
            timecnt = 0
    cello_c_chord.instruments.append(cello)
    print('Composing ' + filename.split('/')[-1].split('.')[0] + '.mid')
    cello_c_chord.write(output_path + filename.split('/')[-1].split('.')[0] + '加停顿.mid')
