import numpy as np
import yaml
from os.path import join
from glob import glob
import shutil
from scipy.io import wavfile
import random
random.seed(10)

audio_src_path = '/Users/alistaircarson/projects/delay_modulation_afx/audio/mod_fx_listening_test'
audio_dest_path = 'configs/resources/audio/mod_fx_listening_test/'
shutil.copytree(audio_src_path, audio_dest_path, dirs_exist_ok=True)

all_wavs = glob(join(audio_dest_path, '*/*.wav'))

for wav in all_wavs:
    fs, x = wavfile.read(wav)
    x = x * 10 ** (6/20)
    peak = np.max(np.abs(x))
    if peak > 1.0:
        print(peak)
        print(wav)
    assert(peak < 1.0)
    x = np.stack((x, x), axis=-1)
    wavfile.write(wav, fs, x)

mushra_path = 'configs/mod_fx_template.yaml'


with open(mushra_path, 'r') as file:
    d = yaml.safe_load(file)


TYPE = 'mushra'


pedals = ['SS-B', 'SS-E', 'SV-1-E', 'BF-2-A', 'BF-2-C']
#clip_options = [1, 2, 3, 4, 5, 6, 7]
#guitar_clips = np.arange(1, 7)
guitar_clips = [1, 2, 3]
#bass_clips = np.arange(7, 13)

np.random.shuffle(guitar_clips)
#np.random.shuffle(bass_clips)


stimuli_keys = ['model']

pages = []

pages.append('')
pages.append('random')

for i, pedal in enumerate(pedals):
    # n = np.random.randint(0, 7, size=(2))
    # print(n)
    #clips = [guitar_clips[i], bass_clips[i]]
    clips = random.sample(guitar_clips, 3)

    print(clips)
    for clip in clips:
        stimuli = {'anchor': join(audio_dest_path, 'input', f'clip{clip}_input.wav')}

        pedal_dir = pedal[:-2].lower()
        stimuli.update({'C1': join(audio_dest_path, pedal_dir, f'{pedal}_clip{clip}_model.wav')})

        if 'SS' in pedal:
            stimuli.update({'C2': join(audio_dest_path, pedal_dir, f'{pedal}_clip{clip}_reaper.wav')})
        else:
            stimuli.update({'C2': join(audio_dest_path, pedal_dir, f'{pedal}_clip{clip}_pedalboard.wav')})

        page = {'type': 'mushra',
                'id': f'test_{pedal}_{clip}',
                'name': 'TEST IN PROGRESS',
                'content': 'Rate each condition by how closely it matches the reference. '
                           '<br><br> Remember: <em>at least</em> one clip <em>must</em> be rated 100. It is okay to rate more than one clip 100.'
                           '<br><br>Keyboard shortcuts: SPACE - play/pause; R - play/pause reference; NUMBERS - play/pause condition by number; BACKSPACE - stop',
                'enableLooping': True,
                'showConditionNames': False,
                'createAnchor35': False,
                'createAnchor70': False,
                'reference': join(audio_dest_path, pedal_dir, f'{pedal}_clip{clip}_target.wav'),
                'stimuli': stimuli
               }
        pages.append(page)



# add welcome and finish pages
pages.insert(0, d['pages'][1])
pages.insert(0, d['pages'][0])
pages.append(d['pages'][-1])

d['pages'] = pages

with open(mushra_path.replace('template', 'mushra'), 'w') as file:
    yaml.dump(d, file, default_flow_style=False, sort_keys=False)

with open(mushra_path.replace('mod_fx_template', 'default'), 'w') as file:
    yaml.dump(d, file, default_flow_style=False, sort_keys=False)

print(d)







