import subprocess

def Renderer(state):
    
    subprocess.run(
        "npx remotion render src/index.ts TypographyVideo out/video.mp4",
        cwd=r"D:\Projects\Applications\Video-Editing-Pipeline\src\core\video-rendering",
        shell=True
    )