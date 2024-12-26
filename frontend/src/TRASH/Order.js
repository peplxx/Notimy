import React, {useContext} from 'react';
import {css, styled} from 'styled-components';

import {AppContext} from "../../../context/App";
import OrderTop from './OrderTop';
import OrderBottom from './OrderBottom';


const shaking = css`
    0% { transform: translateX(0); }
    25% { transform: translateX(-2%); }
    50% { transform: translateX(0%); }
    75% { transform: translateX(2%); }
    100% { transform: translateX(0%); }
`;

const OrderStyled = styled.div`
    position: relative;
    margin: 1em auto;
    width: 90%;
    z-index: 1;
    text-align: center;
    border-radius: 0.8em;
    font-size: inherit;

    ${({ isOpen }) => isOpen && `
        transition: padding 0.5s;
        padding-top: 60%;
    `}
    ${({ isOpen }) => !isOpen && `
        transition: padding 0.5s;
        padding-top: 30%;
    `}
    ${({ isDeleting }) => isDeleting && `
        animation: ${shaking} .15s .15s;
        animation-iteration-count: 2;
    `}

    span {
        user-select: none;
    }
`;


const Order = ({isOpen, setIsOpen, isDeleting, admin=false}) => {
    // const {setIsOpen, isOpen, isDeleting} = useContext(OrderContext);

    const {deleteOrder} = useContext(AppContext);

    return (
        <OrderStyled
            isOpen={isOpen}
            isDeleting={isDeleting}
            onClick={() => setIsOpen(!isOpen)}
        >
            <OrderTop admin={admin} deleteOrder={deleteOrder}/>
            <OrderBottom admin={admin}/>
        </OrderStyled>
    );
};

export default Order;
