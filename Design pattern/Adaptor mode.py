class Computer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'the {} computer'.format(self.name)

    def execute(self):
        """ call by client code """
        return 'execute a program'


class Synthesizer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'the {} synthesizer'.format(self.name)

    def play(self):
        return 'is playing an electroinc song'


class Human:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'the {} human'.format(self.name)

    def speak(self):
        return 'says hello'


class Adapter:
    def __init__(self, obj, adapted_methods):
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __str__(self):
        return str(self.obj)

def main():
    objs = [Computer('Asus')]
    synth = Synthesizer('moog')
    objs.append(Adapter(synth, dict(execute=synth.play)))
    human = Human('Wnn')
    objs.append(Adapter(human, dict(execute=human.speak)))

    for o in objs:
        print('{} {}'.format(str(o), o.execute()))


if __name__ == "__main__":
    main()