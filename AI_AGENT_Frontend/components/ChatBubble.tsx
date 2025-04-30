type Message = {
  text: string;
  type: "user" | "bot"; // <-- restrict to these exact strings
};

export default function ChatBubble({ text, type }: Message) {
  return (
    <div className={`my-2 ${type === 'user' ? 'text-right' : 'text-left'}`}>
      <div className={`inline-block px-4 py-2 rounded-lg ${type === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'}`}>
        {text}
      </div>
    </div>
  )
}