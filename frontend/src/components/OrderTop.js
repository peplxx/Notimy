import React, {useRef} from "react";
import styled, {css} from "styled-components";

import Slider from "components/Slider";
import Bulb from "components/User/Bulb";

import {TrashBucketSvg} from "components/svg/TrashBucketSvg";
import {AcceptSvg} from "components/svg/AcceptSvg";

const TopStyled = styled.div`
    position: absolute;
    width: 100%;
    top: 0;
    padding-top: 25%;
    box-shadow: 0 0.1em 0.2em rgba(0, 0, 0, 0.6);
    border-radius: inherit;
    z-index: 2;
    ${({backgroundColor}) => backgroundColor || "inherit"};
`;

const TitleStyled = styled.span`
  font-family: "Rubik", sans-serif;
  color: #202123;
  font-weight: 700;
  max-width: 78%;
  text-align: left;
  line-height: 1em;
  position: absolute;
  bottom: 5%;
  left: 5%;
  font-size: 2em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  user-select: none;
`;

const SideStyled = styled.div`
  position: absolute;
  right: 1.3%;
  top: 5%;
  height: 90%;
  width: 13%;
  z-index: 4;
  border-radius: inherit;
  box-shadow: inset 0.2em 0.2em 0.2em rgba(0, 0, 0, 0.4);
  background-color: #202123;
  ${({ isSideOpen }) =>
    isSideOpen
        ? css`
          margin-left: 0.25rem;
          padding-left: 84.1%;
          transition: padding 0.5s;
        `
        : css`
          padding-left: 0;
          transition: padding 0.5s;
        `}
`;

const ExpandSignStyled = styled.span`
  font-family: "Rubik", sans-serif;
  color: white;
  font-weight: 700;
  font-size: 1.5em;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  transform: ${({ isSideOpen }) =>
    isSideOpen ? "translateX(-25%) rotate(180deg)" : "none"};
  transition: transform 0.2s 0s;
`;


const OrderTop = ({
                      order,
                      backgroundStyles,
                      isReady,
                      isSideOpen,
                      setIsSideOpen,
                      setIsOpen,
                      isOpen,
                      deleteOrder,
                      closeOrder,
                      isQrOpen,
                      setIsQrOpen,
                      setQrCode,
                      admin = false
                  }) => {
    // ! Актуальный
    const MenuClickable = useRef(null);

    // ?
    // const emSize = parseFloat(getComputedStyle(document.documentElement).fontSize); // Получаем размер 1em в пикселях
    // const qrSize = 14 * emSize; // Пример: если 10em


    const toggleMenu = () => {
        setIsSideOpen(!isSideOpen);
    };
    // console.log(order)
    const toggleOrder = () => {
        setIsOpen(!isOpen);
    }

    return (
        <TopStyled backgroundColor={backgroundStyles} onClick={toggleOrder}>
            {!admin && <Bulb isReady={isReady}/>}
            <TitleStyled>#{order.code.slice(0, 2)}</TitleStyled>
            <SideStyled
                ref={MenuClickable}
                isSideOpen={isSideOpen}
                onClick={(e) => {
                    toggleMenu();
                    e.stopPropagation();
                }}
            >
                {/* Close (Finish) order */}
                {admin && isSideOpen && !isReady &&
                    <Slider parentRef={MenuClickable} SliderIcon={AcceptSvg} sliderColor={'green'}
                            onDone={closeOrder}/>
                }
                {/* Remove order */}
                {isSideOpen && (!admin || isReady) &&
                    <Slider parentRef={MenuClickable} SliderIcon={TrashBucketSvg} sliderColor={'red'}
                            onDone={deleteOrder}/>
                }

                {/* <span className={styles.code}>{order.code}</span> */}
                {/* TODO fix qr code*/}
                {/*{isSideOpen &&*/}
                {/*    <div*/}
                {/*        className={styles.qrCodeBtn}*/}
                {/*        onClick={(e) => {*/}
                {/*        setQrCode(*/}
                {/*            <QRCodeCanvas value={`https://notimy.ru/j/c/${order.id}`} size={qrSize}/>*/}
                {/*        );*/}
                {/*        e.stopPropagation()*/}
                {/*    }}>*/}
                {/*        QR code*/}
                {/*    </div>*/}
                {/*}*/}

                <ExpandSignStyled isSideOpen={isSideOpen}>{"<"}</ExpandSignStyled>
            </SideStyled>
        </TopStyled>
    );
};

export default OrderTop;
