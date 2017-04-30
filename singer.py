import random, math
import numpy as np
import pandas as pd
import scipy.integrate as integrate
import source, additions

class Singer:
    def __init__(self, duration, adj_per_sec, max_vol = 1, pid_coeffs=None, starting_freq = 300, noise_range = (0,0), control_error_range = (-3,3), flatness = 0):
        self.flatness = flatness
        self.noise_range = noise_range
        self.control_error_range = control_error_range
        self.max_vol = max_vol
        self.duration = duration
        self.adj_per_sec = adj_per_sec
        if pid_coeffs:
            self.pid_coeffs = pid_coeffs
        self.realized = np.zeros(duration)
        self.realized[0] = starting_freq
        self.volumes = np.zeros(duration) #initial volume stays as zero
        self.error_integral = 0
        self.last_error = np.nan
        self.last_target = 0
        self.t = 1
        self.int_space = np.linspace(0, 1/adj_per_sec, 100/adj_per_sec)
    
    def get_last_note(self, t):
        return self.realized[t-1]
    
    def get_error(self, target):
        ''' Calculates current error in order to
            inform a control routine
        '''
        target -= self.flatness
        error = target - self.realized[self.t-1]
        lower, upper = self.noise_range
        noise = random.uniform(lower, upper)
        error = error + noise
        return error
    
    def get_volume(self, error):
        adj = math.log(math.log(abs(error)+math.e)+math.e)
        return self.max_vol # no adjustment
    
    def pid_control(self, error):
        if not self.pid_coeffs:
            raise Exception('no coeffs provided, but using PID')
        kp, ki, kd = self.pid_coeffs
        self.error_integral += (1/self.adj_per_sec)*error
        d_error = (self.last_error - error)*self.adj_per_sec \
                    if not np.isnan(self.last_error) \
                    else 0
        control = kp*error + ki * self.error_integral + kd * d_error
        lower, upper = self.control_error_range
        return control + random.uniform(lower,upper)
    
    def voice_model(self, state_vector, t):
        ''' Model of the effect that singer effort has
            on setting vocal pitch. Singer input on range (-1,1),
            so we simply scale this input to get a simple model of pitch.
        '''
        pitch, singer_input = state_vector
        deriv_of_pitch = singer_input
        deriv_of_control = 0
        return [deriv_of_pitch, deriv_of_control]
    
    def simulate_voice(self, control):
        diffeq_params = [self.realized[self.t-1], control]
        integration_output = integrate.odeint(self.voice_model, 
                                              diffeq_params, 
                                              self.int_space)
        realized_pitches, derivs_of_pitch = integration_output.T
        realized = realized_pitches[-1]
        return realized
    
    def adjustment(self, target):
        # check if need to reset integral
        if target != self.last_target:
            self.error_integral = 0
            self.last_error = np.nan
        # derive control
        error = self.get_error(target)
        control = self.pid_control(error)
        vol = self.get_volume(error)
        
        # simulate applying control
        realized = self.simulate_voice(control)
        
        # bookkeeping
        self.realized[self.t] = realized
        self.volumes[self.t] = vol
        self.last_error = error
        self.last_target = target
        self.t += 1
    def render_singing(self):
        pitch_duration = 1/self.adj_per_sec
        sounds = []
        starting_phase = random.random()
        for t in range(self.duration):
            phase = additions.get_phase(sounds[-1], new_volume=self.volumes[t]) if len(sounds) > 0 else starting_phase
            sounds.append(self.volumes[t] * source.sine(self.realized[t], pitch_duration, phase=phase))
        sound = np.concatenate([s[:-1] for s in sounds])
        return sound
        