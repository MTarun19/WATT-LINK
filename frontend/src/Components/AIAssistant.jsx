import React, { useState } from "react";
import {
    Bot,
    Send,
    Sparkles,
    Cpu
} from "lucide-react";

import "./AIAssistant.css";

export default function AIAssistant() {

    const [messages, setMessages] = useState([
        {
            sender: "ai",
            text: "Hello Tarun 👋 I'm WATT AI. Ask me anything about your smart microgrid."
        }
    ]);

    const [input, setInput] = useState("");

    const sendMessage = async () => {

        if (!input.trim()) return;

        const userMessage = {
            sender: "user",
            text: input
        };

        setMessages(prev => [...prev, userMessage]);

        // Temporary AI response
        const aiMessage = {
            sender: "ai",
            text: "Thinking..."
        };

        setMessages(prev => [...prev, userMessage, aiMessage]);

        try {

            // Later connect to FastAPI

            /*
            const response = await fetch("http://127.0.0.1:8000/ai/chat",{
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    message:input
                })
            });

            const data = await response.json();
            */

            setTimeout(() => {

                setMessages(prev => {

                    const temp = [...prev];

                    temp[temp.length - 1] = {

                        sender: "ai",

                        text:
                            "I'm monitoring your batteries, sensors, marketplace and ESP32 devices. Soon I'll answer using real-time data."

                    };

                    return temp;

                });

            }, 1000);

        }

        catch {

            setMessages(prev => {

                const temp = [...prev];

                temp[temp.length - 1] = {

                    sender: "ai",

                    text: "Unable to contact AI server."

                };

                return temp;

            });

        }

        setInput("");

    };

    return (

        <div className="assistant">

            <div className="assistant-header">

                <Bot size={22}/>

                <div>

                    <h3>WATT AI</h3>

                    <span>

                        <Cpu size={12}/>

                        Monitoring Microgrid

                    </span>

                </div>

            </div>

            <div className="assistant-body">

                {messages.map((msg,index)=>(

                    <div

                        key={index}

                        className={`message ${msg.sender}`}

                    >

                        {msg.sender==="ai" &&

                            <Sparkles size={16}/>

                        }

                        <p>{msg.text}</p>

                    </div>

                ))}

            </div>

            <div className="assistant-input">

                <input

                    value={input}

                    onChange={(e)=>setInput(e.target.value)}

                    placeholder="Ask anything..."

                    onKeyDown={(e)=>{

                        if(e.key==="Enter") sendMessage();

                    }}

                />

                <button onClick={sendMessage}>

                    <Send size={18}/>

                </button>

            </div>

        </div>

    );

}