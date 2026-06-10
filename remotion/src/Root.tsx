// Root.tsx
import "./index.css";
import { Composition, getInputProps } from "remotion";
import { MyComposition } from "./Composition";

interface VideoProps {
  headline?: string;
  subheading?: string;
  durationInFrames?: number;
}

export const RemotionRoot: React.FC = () => {
  // Capture dynamic inputs from your Python script with clean fallback text
  const {
    headline = "QUANTUM BREEDER",
    subheading = "Extracting maximum structural energy efficiency via closed loop cycles.",
    durationInFrames = 900, // Default 30 seconds at 30fps
  } = getInputProps() as VideoProps;

  return (
    <>
      <Composition
        id="MyComp"
        component={MyComposition}
        durationInFrames={durationInFrames}
        fps={30}
        width={1080}  // 1080x1920 is standard vertical format for shorts/reels
        height={1920}
        defaultProps={{
          headline,
          subheading,
        }}
      />
    </>
  );
};