import speech_recognition as sr 
from os import path
from pydub import AudioSegment
import progressbar as pb

def convert(input,outputfile):
    src = input
    dst = "dst.wav"

    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")



    sound = AudioSegment.from_file('dst.wav')
    total = len(sound)
    seg = 3000
    percent = total//3000
    print(len(sound))
    exit
    start=0
    end = 0
    str = ''
    count = 0
    if percent==0:
        r = sr.Recognizer()
        harvard = sr.AudioFile('first.wav')
        with harvard as source:
            audio = r.record(source)

        str+=r.recognize_google(audio)
        with open(outputfile,'w') as out:
            out.write(str)
        exit
    else:
        
        widgets = ['Total {} files: '.format(percent), pb.Percentage(),' ',pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
        timer = pb.ProgressBar(widgets=widgets, maxval=percent).start()
        while end<len(sound):
            try:
                start = end
                end += seg
                first = sound[start:end]
                first.export('first.wav',format="wav")

                r = sr.Recognizer()

                
                harvard = sr.AudioFile('first.wav')
                with harvard as source:
                    audio = r.record(source)

                str+=r.recognize_google(audio)
                count+=1
                timer.update(count)
            except:
                print('no words')

        with open(outputfile,'w') as out:
            out.write(str)

convert("audio.mp3",'output.txt')