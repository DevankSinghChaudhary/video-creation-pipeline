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
const WORDS_PER_SCENE = 8;

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
  const frame = useCurrentFrame();
  const currentTime = frame / FPS;

  const currentWordIndex = timing.findIndex(
  (word) => currentTime < word.end
  );

  const sceneIndex =
    currentWordIndex === -1
      ? 0
      : Math.floor(currentWordIndex / WORDS_PER_SCENE);

  const visibleWords = timing.slice(
    sceneIndex * WORDS_PER_SCENE,
    (sceneIndex + 1) * WORDS_PER_SCENE
  );

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#eeeeee"
      }}
    >
      <Html5Audio
        src={staticFile("voice.mp3")} volume={0.7} 
        />
       <Html5Audio 
        src={staticFile("background.mp3")} volume={0.08}
      />

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          alignItems: "center",
          fontSize: 60,
          fontWeight: 800,
          color: "#0088cc",
          fontFamily: "monospace",
          maxWidth: "80%",
          textAlign: "center",
          lineHeight: 1.2
        }}
      >
        {visibleWords.map((word, index) => (
          <WordBlock key={index} word={word} />
        ))}
      </div>
    </AbsoluteFill>
  );
};