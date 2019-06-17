# Used to list all of the currently implemented tests
# in the test suite

class tests():

    def __init__(self):
        self.suites = []
        self.env_names = []

        # Get all OpenAIGym Envs        
        try:
            from gym import envs
            all_envs = envs.registry.all()
            for entry in all_envs:
                self.suites.append('OpenAIGym')
                self.env_names.append(entry.id)
        except Exception as e:
            print(e)
    
        # Get all default ViZDoom Envs        
        try:
            import vizdoom
            # Env name must match name in scenario folder!
            all_envs = ['basic', 'deadly_corridor', 'defend_the_center',
                        'defend_the_line', 'health_gathering', 
                        'predict_position', 'take_cover']
            for entry in all_envs:
                self.suites.append('ViZDoom')
                self.env_names.append(entry)
        except Exception as e:
            print(e)
        
    def list_all(self):
        return self.suites, self.env_names

