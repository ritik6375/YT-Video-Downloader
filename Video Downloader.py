import webview
import subprocess
import os
import json
import pymsgbox



class Api:
    def close_fx(self):
        window.destroy()
        exit()

    # to download video and audio then merge
    def download_video(self, url, save_path, exe_path="yt-dlp.exe"):

        command = [
            exe_path,
            '-f', 'bestvideo+bestaudio',
            '--merge-output-format', 'mp4',
            '-o', os.path.join(save_path, '%(title)s.%(ext)s'),
            '--newline',  #progress prints line by line
            url
        ]

        # runs command and capture the output line by line. stdout: standard output, stderr: standard error, PIPE: redirect cmd output to python
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # loop through the output to print progress
        for line in process.stdout:
            if '%' in line:
                #extract percentage from output
                progress = line.split()[1].replace("%", "")  #split line words in array and choose 2nd. Ex:- [download] 10% of   10.25MiB
                print(f"Download progress: {progress}")
                window.evaluate_js(f"document.querySelector('.ui-progressbar-value').style.width = '{progress}%';")


        print("Download completed successfully!")
        pymsgbox.alert('Download completed successfully!')



    def get_video_metadata(self, url, exe_path="yt-dlp.exe"):

        command = [
            exe_path,
            '--dump-json',
            url
        ]

        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if process.returncode == 0:
            metadata = json.loads(process.stdout)
            title = metadata.get('title', 'N/A')
            thumbnail = metadata.get('thumbnail', 'N/A')
            print("Title:", title)
            print("Thumbnail:", thumbnail)
            element1 = window.dom.get_element('#title')
            element1.empty()
            element1.append(title)

            element2 = window.dom.get_element('#thumbnail')
            element2.attributes['src'] = thumbnail

            #-- execute download function
            api.download_video(url, './')

        else:
            print("Error occurred:", process.stderr)
            pymsgbox.alert('Error occurred!')



api = Api()
window = webview.create_window('Video Downloader', 'frontend/index.html', width=510, height=420, resizable=False, zoomable=False, js_api=api, text_select=False, minimized=False, maximized=False, frameless=True, easy_drag=True)
webview.start()