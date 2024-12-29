import React, { useEffect, useRef, useState } from "react";
import styled, { css } from "styled-components";
import { Bulb } from "components/Bulb";
import Slider from "components/Slider";
import { TrashBucketSvg } from "components/svg/TrashBucketSvg";

const TopStyled = styled.div`
  position: absolute;
  width: 100%;
  top: 0;
  padding-top: 25%;
  box-shadow: 0 0.1em 0.2em rgba(0, 0, 0, 0.6);
  border-radius: inherit;
  z-index: 2;
  background-color: ${({ backgroundColor }) => backgroundColor || "inherit"};
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

const OrderTop = ({ code, deleteOrder, backgroundColorStyles, admin = false }) => {
    const MenuClickable = useRef(null);
    const titleRef = useRef(null);
    const [isSideOpen, setIsSideOpen] = useState(false);

    useEffect(() => {
        const resizeTextToFit = () => {
            if (titleRef.current) {
                let fontSize = 2; // Starting size
                titleRef.current.style.fontSize = fontSize + "em";

                while (
                    titleRef.current.scrollWidth > titleRef.current.offsetWidth &&
                    fontSize > 0.5
                    ) {
                    fontSize -= 0.1;
                    titleRef.current.style.fontSize = fontSize + "em";
                }
            }
        };

        resizeTextToFit();
        window.addEventListener("resize", resizeTextToFit);

        return () => {
            window.removeEventListener("resize", resizeTextToFit);
        };
    }, []);

    const toggleMenu = () => {
        setIsSideOpen(!isSideOpen);
    };

    return (
        <TopStyled backgroundColor={backgroundColorStyles}>
            <Bulb />
            <TitleStyled ref={titleRef}>#{code.slice(0, 2)}</TitleStyled>
            <SideStyled
                ref={MenuClickable}
                isSideOpen={isSideOpen}
                onClick={(e) => {
                    toggleMenu();
                    e.stopPropagation();
                }}
            >
                {isSideOpen ? (
                    <Slider
                        onDone={deleteOrder}
                        sliderColor={"red"}
                        SliderIcon={TrashBucketSvg}
                        parentRef={MenuClickable}
                    />
                ) : null}
                <ExpandSignStyled isSideOpen={isSideOpen}>{"<"}</ExpandSignStyled>
            </SideStyled>
        </TopStyled>
    );
};

export default OrderTop;
