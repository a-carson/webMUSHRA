import yaml
from os.path import join
import shutil

audio_src_path = '/Users/alistaircarson/audio_datasets/dist_fx_feb25_v2/listening_test'
audio_dest_path = 'configs/resources/audio/aa_listening_test/'
shutil.copytree(audio_src_path, audio_dest_path, dirs_exist_ok=True)

mushra_path = '../webMUSHRA/configs/aa_test_template.yaml'


with open(mushra_path, 'r') as file:
    d = yaml.safe_load(file)


TYPE = 'mushra'

training_clips = ['bass_1']
training_device = 'broadcast'
test_clips = [
              'sweep_log',
              'sweep_10k',
              'sweep_20k',
              'bass_2',
              'guitar_1',
              'guitar_2']
test_devices = ['broadcast', 'gypsy']

cab_keys = ['']

stimuli_keys = ['lstm_og', 'lstm_aa', 'wavenet_og', 'wavenet_aa']

pages = []

for clip in training_clips:

    stimuli = {'anchor': join(audio_dest_path, clip, 'anchor.wav')}
    for s in stimuli_keys:
        stimuli[s] = join(audio_dest_path, clip, f'{training_device}_{s}.wav')

    page = {'type': 'mushra',
            'id': f'training_{training_device}_{clip}',
            'name': 'Training example',
            'content': 'This is a training example to show you how to use the user interface. Your results will not be recorded. '
                       '<br><br> Rate each condition below by how closely it sounds like the reference. Try consider both differences in <em>timbre</em> and the presence of <em>artefacts</em> when making your judgments. You can give multiple conditions the same score.  '
                       '<br><br> Useful keyboard shortcuts: SPACE - play/pause; R - play/pause reference; NUMBERS - play/pause condition by number; BACKSPACE - stop.'
                       '<br><br> Feel free to listen as many times as you need and to loop segments.',
            'enableLooping': True,
            'showConditionNames': False,
            'createAnchor35': False,
            'createAnchor70': False,
            'reference': join(audio_dest_path, clip, f'{training_device}_target.wav'),
            'stimuli': stimuli
           }

    pages.append(page)

pages.append('')
pages.append('random')

for clip in test_clips:

    for device in test_devices:
        for cab in cab_keys:
            stimuli = {'anchor': join(audio_dest_path, clip, f'anchor{cab}.wav')}
            for s in stimuli_keys:
                stimuli[s] = join(audio_dest_path, clip, f'{device}_{s}{cab}.wav')

            page = {'type': 'mushra',
                    'id': f'test_{device}_{clip}{cab}',
                    'name': 'TEST IN PROGRESS',
                    'content': 'Rate each condition by how closely it matches the reference. '
                               '<br><br>Keyboard shortcuts: SPACE - play/pause; R - play/pause reference; NUMBERS - play/pause condition by number; BACKSPACE - stop',
                    'enableLooping': True,
                    'showConditionNames': False,
                    'createAnchor35': False,
                    'createAnchor70': False,
                    'reference': join(audio_dest_path, clip, f'{device}_target{cab}.wav'),
                    'stimuli': stimuli
                   }

            pages.append(page)

#pages = pages[0:4]

# add welcome and finish pages
pages.insert(0, d['pages'][0])
pages.append(d['pages'][-1])

d['pages'] = pages

with open(mushra_path.replace('template', 'auto_gen'), 'w') as file:
    yaml.dump(d, file, default_flow_style=False, sort_keys=False)

print(d)







