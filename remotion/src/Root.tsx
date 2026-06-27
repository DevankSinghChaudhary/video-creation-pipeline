// Root.tsx
import "./index.css";
import { Composition, getInputProps } from "remotion";
import { MyComposition, durationInFrame } from "./Composition";

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
    durationInFrames = durationInFrame,
  } = getInputProps() as VideoProps;

  return (
    <>
      <Composition
        id="MyComp"
        component={MyComposition}
        durationInFrames={durationInFrames}
        fps={30}
        width={1080} 
        height={1920}
        defaultProps={{
          headline,
          subheading,
        }}
      />
    </>
  );
};