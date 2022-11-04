import os
import pretty_midi

filenotenum = 25
musicdir = 'TrainSet/39midi/'
outputdir = 'TrainSet/equilong' + str(filenotenum) + '/'
os.makedirs(outputdir)

for song in os.listdir(musicdir):
    if song.split('.')[-1] == 'mid':
        filename = musicdir + song
        midi_data = pretty_midi.PrettyMIDI(filename)
        notes = midi_data.instruments[0].notes
        os.makedirs(outputdir + song)
        for i in range(len(notes) - filenotenum + 1):
            cello_c_chord = pretty_midi.PrettyMIDI()
            cello_program = pretty_midi.instrument_name_to_program('Flute')
            cello = pretty_midi.Instrument(program=cello_program)
            cello.notes = notes[i:i+filenotenum]
            cello_c_chord.instruments.append(cello)
            cello_c_chord.write(outputdir + song + '/' + str(i) + '.mid')
        print('Finish ' + song)
    