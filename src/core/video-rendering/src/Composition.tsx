import React from "react";
import Scene from "./scene.json";
import {
  AbsoluteFill,
  useCurrentFrame,
  Html5Audio,
  staticFile
} from "remotion";

type TimingWord = {
  word: string;
  start: number;
  end: number;
};

const FPS = 30;

const timing: TimingWord[] = Scene;

const WordBlock: React.FC<{ word: TimingWord }> = ({ word }) => {
  const frame = useCurrentFrame();
  const currentTime = frame / FPS;

  if (currentTime < word.start) {
    return null;
  }

  return (
    <span
      style={{
        marginRight: 20
      }}
    >
      {word.word}
    </span>
  );
};

export const TypographyVideo: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#EDEADE"
      }}
    >
      <Html5Audio src={staticFile("voice.mp3")} 
        volume={1}
        />

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          alignItems: "center",
          fontSize: 95,
          fontWeight: 800,
          color: "#880808",
          fontFamily: "system-ui",
          maxWidth: "80%",
          textAlign: "center",
          lineHeight: 1.2
        }}
      >
        {timing.map((word, index) => (
          <WordBlock key={index} word={word} />
        ))}
      </div>
    </AbsoluteFill>
  );
};