import React from 'react';
import {BrowserRouter as Router, Navigate, Route, Routes} from 'react-router-dom';
import JoinChannelSpot from "./pages/JoinChannelSpot";
import JoinChannel from "./pages/JoinChannel";
import AdminLogin from "./pages/AdminLogin";
import Landing from "./pages/landing";
import UUIDLogin from "./pages/UUID";
import MainApp from "pages/App/MainApp";


function App() {
    // Main Entry
    return (
        <Router basename="/app">
            <Routes>
                {/*<Route path="/" element={<Landing/>}/>*/}
                <Route path="/" element={<MainApp/>}/>
                <Route path="/:token" element={<UUIDLogin/>}/>
                <Route path="/admin/login/:token" element={<AdminLogin/>}/>
                <Route path="/j/:id" element={<JoinChannelSpot/>}/>
                <Route path="/j/c/:id" element={<JoinChannel/>}/>
                <Route path="*" element={<Navigate to="/"/>}/>
            </Routes>
        </Router>
    );
}

export default App;
