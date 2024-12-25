import React from 'react';
import {BrowserRouter as Router, Navigate, Route, Routes} from 'react-router-dom';
import JoinChannelSpot from "./pages/JoinChannelSpot";
import JoinChannel from "./pages/JoinChannel";
import AdminLogin from "./pages/AdminLogin";
import Landing from "./pages/landing";
import UUIDLogin from "./pages/UUID";
import MainApp from "./pages/MainApp";
import {AppContextProvider} from "./context/App";


function App() {
    // Main Entry
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Landing/>}/>
                <Route path="/app" element={<MainApp/>}/>
                <Route path="/app/:token" element={<UUIDLogin/>}/>
                <Route path="/app/admin/login/:token" element={<AdminLogin/>}/>
                <Route path="/j/:id" element={<JoinChannelSpot/>}/>
                <Route path="/j/c/:id" element={<JoinChannel/>}/>
                <Route path="*" element={<Navigate to="/"/>}/>
            </Routes>
        </Router>
    );
}

export default App;
