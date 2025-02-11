import React, {useEffect} from 'react';
import {useParams, useNavigate} from 'react-router-dom';
import {joinChannel} from "../utils/api";

const JoinChannel = () => {
    const {id} = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        const joinAndNavigate = async () => {
            try {
                await joinChannel(id);
                navigate('/app'); // Redirect after joining the channel
            } catch (error) {
                console.error("Failed to join channel", error);
                // Handle error as needed
            }
        };

        joinAndNavigate();
    }, [id, navigate]);

    return <div>adding channel</div>;
};

export default JoinChannel;
