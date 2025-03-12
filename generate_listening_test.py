import yaml
from os.path import join
import shutil

audio_src_path = '/Users/alistaircarson/audio_datasets/dist_fx_feb25_v2/listening_test'
audio_dest_path = 'configs/resources/audio/aa_listening_test/'
shutil.copytree(audio_src_path, audio_dest_path, dirs_exist_ok=True)

mushra_path = 'configs/afx_template.yaml'


with open(mushra_path, 'r') as file:
    d = yaml.safe_load(file)


TYPE = 'mushra'

training_clips = ['bass_1']
training_device = 'broadcast'

test_clips = {
    'broadcast': [
              'sweep_10k',
              'sweep_20k',
              'bass_2',
              'bass_3',
              'guitar_1',
              'guitar_2'],
    'gypsy': [
        'sweep_10k',
        'sweep_20k',
        'bass_5',
        'bass_6',
        'guitar_3',
        'guitar_4'],
}

stimuli_keys = ['lstm_og', 'lstm_aa', 'wavenet_og', 'wavenet_aa']

pages = []

pages.append('')
pages.append('random')

for device, clips in test_clips.items():
    for clip in clips:
        stimuli = {'anchor': join(audio_dest_path, clip, f'anchor.wav')}
        for i, s in enumerate(stimuli_keys):
            stimuli[f'C{i+1}'] = join(audio_dest_path, clip, f'{device}_{s}.wav')

        page = {'type': 'mushra',
                'id': f'test_{device}_{clip}',
                'name': 'TEST IN PROGRESS',
                'content': 'Rate each condition by how closely it matches the reference. '
                           '<br><br>Keyboard shortcuts: SPACE - play/pause; R - play/pause reference; NUMBERS - play/pause condition by number; BACKSPACE - stop',
                'enableLooping': True,
                'showConditionNames': False,
                'createAnchor35': False,
                'createAnchor70': False,
                'reference': join(audio_dest_path, clip, f'{device}_target.wav'),
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

with open(mushra_path.replace('afx_template', 'default'), 'w') as file:
    yaml.dump(d, file, default_flow_style=False, sort_keys=False)

print(d)







