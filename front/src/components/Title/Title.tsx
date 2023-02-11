type TitleProps = { text: string };

export function Title({ text }: TitleProps) {
  return (
    <h1 className="text-3xl text-center font-bold font-sans mb-8 text-gray-600">
      {text}
    </h1>
  );
}
