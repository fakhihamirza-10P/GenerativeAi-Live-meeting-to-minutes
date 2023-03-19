import speech_recognition as sr
import moviepy.editor as mp
import subprocess
import openai
import datetime
import shutil
import argparse
import os

def extractText(meeting_name):
    with open(meeting_name + ".txt", "r", encoding="utf-8") as f:
        text = f.read()
    return text
    
def getMinutes(meeting_name):
    openai.api_key = "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"

    model_engine = "gpt-3.5-turbo"
    transcript = extractText(meeting_name)
    prompt_text = ["Create meeting minutes from the follwing transcription and include decisions made, make sure to highlight any deadlines or important information mentioned during the meeting ","extract sprint items or sprint tasks or backlog items or backlog tasks along with time estimates ","Create action items from this transcript ", "Summarize the following transcript "]
    folder_name = ['meeting_minutes', "backlog_tasks", "action_items", "summary"]
    # prompt = 
    for i,prompt in enumerate(prompt_text):
        data = {"role": "user", "content": prompt + "\n" + transcript}

        response = openai.ChatCompletion.create(model=model_engine,messages=[data])

        if response.choices:
            now = datetime.datetime.now()
            filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"

            text = response.choices[0].message.content

            with open(filename, "w") as f:
                f.write(text)
            
            destination_folder = "/home/ramsha/assemblyai-and-python-in-5-minutes/" + folder_name[i] + "/"
            shutil.move(filename, destination_folder + filename)
            print("Done")
        else:
            print("No response from API.")

def run_python_command(meeting_name):
    command = ["python3", "transcribe.py", meeting_name  , "--local" , "--api_key=c77887b715724b1cb2b2772ad140def8" ]
    subprocess.call(command)

# ================================== START =================================

# read the video file and extract the audio
parser = argparse.ArgumentParser()
parser.add_argument('recording_path', help='url to file or local audio filename')
args = parser.parse_args()
clip = mp.VideoFileClip(args.recording_path)
meeting_name = os.path.basename(args.recording_path)
meeting_name = meeting_name.split('.mp4')
audio = clip.audio.to_audiofile( meeting_name[0] + ".wav")
# run_python_command(meeting_name[0] + ".wav")
getMinutes(meeting_name[0])
