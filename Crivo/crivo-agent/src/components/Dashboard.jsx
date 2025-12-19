import { useState, useEffect } from 'react';
import Sidebar from './Sidebar';
import ChatInterface from './ChatInterface';
import SettingsModal from './SettingsModal';
import ToolsPanel from './ToolsPanel';
import './Dashboard.css';

const Dashboard = ({ user, onLogout }) => {
    // Initial State: Empty, wait for fetch
    const [chats, setChats] = useState([]);
    const [currentChatId, setCurrentChatId] = useState(null);
    const [showSettings, setShowSettings] = useState(false);
    const [showTools, setShowTools] = useState(false);

    // Fetch Chats on Load
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

    useEffect(() => {
        if (user && user.email) {
            fetch(`${API_URL}/api/chats?email=${user.email}`)
                .then(res => res.json())
                .then(data => {
                    setChats(data);
                    if (data.length > 0) {
                        setCurrentChatId(data[0].id);
                    }
                })
                .catch(err => console.error("Error fetching chats:", err));
        }
    }, [user]);

    // Save Chats Helper
    const saveChats = (newChats) => {
        if (user && user.email) {
            fetch(`${API_URL}/api/chats`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: user.email, chats: newChats })
            }).catch(err => console.error("Error saving chats:", err));
        }
    };

    const getCurrentChat = () => chats.find(c => c.id === currentChatId) || (chats.length > 0 ? chats[0] : null);

    const createNewChat = () => {
        const newChat = {
            id: Date.now(),
            title: 'New Chat',
            createdAt: Date.now(),
            content: null
        };
        const updatedChats = [newChat, ...chats];
        setChats(updatedChats);
        setCurrentChatId(newChat.id);
        saveChats(updatedChats);
    };

    const updateCurrentChat = (data) => {
        const updatedChats = chats.map(chat => {
            if (chat.id === currentChatId) {
                let title = chat.title;

                // Generate title based on mode
                if (data.mode === 'deep-research' && data.companyName) {
                    title = `${data.companyName} Research`;
                } else if (data.mode === 'rag' && data.ragPrompt) {
                    // Extract first few words from RAG prompt
                    const words = data.ragPrompt.trim().split(/\s+/).slice(0, 5).join(' ');
                    title = words.length > 30 ? words.substring(0, 30) + '...' : words;
                } else if (data.mode === 'checklist') {
                    // Use a descriptive title for checklist mode
                    title = 'Investment Memo Analysis';
                }

                return { ...chat, ...data, title };
            }
            return chat;
        });
        setChats(updatedChats);
        saveChats(updatedChats);
    };

    const switchChat = (id) => {
        setCurrentChatId(id);
    };

    const deleteChat = (id) => {
        if (!user || !user.email) return;

        // Optimistic UI Update
        const updatedChats = chats.filter(c => c.id !== id);
        setChats(updatedChats);

        // If deleted current chat, switch to first available or reset
        if (id === currentChatId) {
            if (updatedChats.length > 0) {
                setCurrentChatId(updatedChats[0].id);
            } else {
                // If all deleted, create new empty one? Or just null
                createNewChat(); // This might be better UX, to always have one
            }
        }

        // API Call
        fetch(`${API_URL}/api/chats/${id}?email=${user.email}`, {
            method: 'DELETE'
        }).catch(err => {
            console.error("Error deleting chat:", err);
            // Revert on error? For now, simpler implies no revert logic for MVP
        });
    };

    return (
        <div className="dashboard-container">
            <Sidebar
                chats={chats}
                currentChatId={currentChatId}
                onNewChat={createNewChat}
                onSwitchChat={switchChat}
                onDeleteChat={deleteChat}
                onSettings={() => setShowSettings(true)}
                onLogout={onLogout}
            />
            <SettingsModal
                isOpen={showSettings}
                onClose={() => setShowSettings(false)}
                user={user}
            />
            <main className="main-content">
                <header className="top-bar">
                    <div className="brand-header">
                        {/* Breadcrumbs or Title could go here */}
                    </div>
                    <div className="user-actions">
                        <button className="btn-invite">✨ Invite a friend</button>
                        <span className="badge-pro">PRO</span>
                        <div className="user-avatar">
                            <img src="https://ui-avatars.com/api/?name=Andrea&background=random" alt="User" />
                        </div>
                    </div>
                </header>

                <ChatInterface
                    user={user}
                    currentChat={getCurrentChat()}
                    onUpdateChat={updateCurrentChat}
                    onNewChat={createNewChat}
                    onToggleTools={() => setShowTools(true)}
                />

                <SettingsModal isOpen={showSettings} onClose={() => setShowSettings(false)} />
                <ToolsPanel isOpen={showTools} onClose={() => setShowTools(false)} />
            </main>
        </div>
    );
};

export default Dashboard;
