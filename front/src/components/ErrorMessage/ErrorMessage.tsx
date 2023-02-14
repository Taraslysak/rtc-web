interface IErrorMessageProps {
  message: string;
}

export function ErrorMessage({ message }: IErrorMessageProps) {
  return (
    <div
      className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-5"
      role="alert"
    >
      <strong className="font-bold">{message}</strong>
    </div>
  );
}
