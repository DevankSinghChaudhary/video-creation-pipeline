import { Composition } from "remotion";
import { TypographyVideo } from "./Composition";
import Scene from "./scene.json";

const duration = Math.ceil(
  Math.max(...Scene.map((w) => w.end)) * 30
) + 30;

export const Root = () => {
  return (
    <Composition
      id="TypographyVideo"
      component={TypographyVideo}
      durationInFrames={duration}
      fps={30}
      width={1080}
      height={1920}
    />
  );
};