import React from 'react';
import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import Index from 'pages/Index';
import JoinChannel from "./pages/JoinChannel";
import Admin from "./pages/Admin";
import AdminLogin from "./pages/AdminLogin";

function App() {
    return (
        <Router>
            <Routes>
                    <Route path="/" element={<div style={{color: "white", position: "absolute", top: "50%", left: "30%"}}>Скоро здесь появится информация</div>}/>
                <Route path="/app" element={<Index/>}/>
                <Route path="/j/:id" element={<JoinChannel/>}/>
                <Route path="app/admin/login/:token" element={<AdminLogin/>} />
                <Route path="app/admin" element={<Admin/>} />
                <Route path="*" element={<Navigate to="/"/>}/>
            </Routes>
        </Router>
    );
}

export default App;
