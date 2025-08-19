import React, { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatBoxRef = useRef(null);

  // Auto-scroll to bottom whenever chatLog changes
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [chatLog]);

  const handleQuery = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    const userMessage = { role: "user", content: question };
    setChatLog((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: question }),
      });

      const data = await response.json();
      let resultText = "";

      // Handle greetings or fallback messages
      if (data.message) {
        resultText = data.message;
      }
      // Handle errors
      else if (data.error) {
        resultText = "❌ Error: " + data.error;
      }
      // Handle valid results
      else if (data.result && data.result.length > 0) {
        resultText = `🧠 Results for "${question}":\n\n`;
        resultText += data.result
          .map((row, i) => {
            let line = `${i + 1}. `;
            const keys = Object.keys(row);

            // If row has nested object (node)
            if (typeof row[keys[0]] === "object" && row[keys[0]] !== null) {
              const prop = row[keys[0]];
              const fields = [];
              for (const key in prop) {
                if (prop[key] !== null && prop[key] !== undefined) {
                  fields.push(`${key}: ${prop[key]}`);
                }
              }
              line += fields.join(" | ");
            } else {
              // Scalar value (like count)
              line += keys.map((key) => `${key}: ${row[key]}`).join(" | ");
            }

            return line;
          })
          .join("\n");

        if (data.cypher) {
          resultText += `\n\n🔍 Query used:\n${data.cypher}`;
        }
      } else {
        resultText = "❌ No results found. Try rephrasing your question.";
      }

      const botMessage = { role: "bot", content: resultText };
      setChatLog((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error(error);
      setChatLog((prev) => [
        ...prev,
        { role: "bot", content: "❌ Error talking to backend." },
      ]);
    }

    setQuestion("");
    setLoading(false);
  };

  return (
    <div className="app-container">
      <h2>💬 Piyush Chat Application</h2>

      <div className="chat-box" ref={chatBoxRef}>
        {chatLog.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <pre>{msg.content}</pre>
          </div>
        ))}
        {loading && <div className="message bot">🤔 Thinking...</div>}
      </div>

      <form className="input-form" onSubmit={handleQuery}>
        <input
          type="text"
          placeholder="Ask something like: who lives in Mumbai?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default App;
