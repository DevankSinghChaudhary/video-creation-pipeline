import subprocess
from core.nodes.retries import with_retry

@with_retry
def Renderer(state):

    print(f'[Renderer] Started Processing')
    
    subprocess.run(
        "npx remotion render src/index.ts TypographyVideo out/video.mp4",
        cwd=r"D:\Projects\Applications\Video-Editing-Pipeline\src\core\video-rendering",
        shell=True
    )
    print(f'[Renderer] Finished Successfully')