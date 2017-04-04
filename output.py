# cobbling together and updating to python3 useful code from python-musical

import pygame, encode

def play(data, rate=44100):
    ''' Send audio array to pygame for playback
    '''
    pygame.mixer.init(rate, -16, 1, 1024)
    sound = pygame.sndarray.numpysnd.make_sound(encode.as_int16(data))
    length = sound.get_length()
    sound.play()
    pygame.time.wait(int(length * 1000))
    pygame.quit()

def save_wave(data, path, rate=44100):
    ''' Save audio data to wave file, currently only 16bit
    '''
    import wave
    fp = wave.open(path, 'w')
    fp.setnchannels(1)
    fp.setframerate(rate)
    fp.setsampwidth(2)
    fp.setnframes(len(data))
    data = encode.as_int16(data)
    fp.writeframes(data.tostring())
    fp.close()