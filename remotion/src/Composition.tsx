// Composition.tsx
import React from "react";
import json from "./schema.json"


interface MyCompositionProps {
  headline: string;
  subheading: string;
}

export const durationInFrame = 300

export const MyComposition: React.FC<MyCompositionProps> = ({
  headline,
  subheading,
}) => {
  return (
    <div className="w-full h-full bg-neutral-950 text-white flex flex-col justify-center p-16 relative font-sans">
      
      {/* A clean, subtle vector grid pattern overlay for a tech/documentary feel */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1f1f1f_1px,transparent_1px),linear-gradient(to_bottom,#1f1f1f_1px,transparent_1px)] bg-[size:4rem_4rem] opacity-30 z-0" />
      
      {/* Content Container */}
      <div className="z-10 space-y-6 max-w-4xl">
        <h1 className="text-7xl font-black tracking-tight text-emerald-400 uppercase leading-none">
          {headline}
        </h1>
        <p className="text-3xl text-zinc-400 font-light leading-relaxed">
          {subheading}
        </p>
      </div>

    </div>
  );
};