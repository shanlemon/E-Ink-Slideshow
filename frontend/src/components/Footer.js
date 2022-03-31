import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { FaArrowAltCircleUp } from 'react-icons/fa';

const FooterContainer = styled.div`
  color: white;
  background-color: black;
  text-decoration: none;
`;

const Content = styled.div`
  display: flex;
  margin: 4rem 0 4rem 8rem;
  @media screen and (max-width: 960px) {
    flex-direction: column;
    margin: 1rem 0 1rem 2rem;
  }
`;

const InfoPanel = styled.div`
  display: flex;
  width: 30%;
  flex-direction: column;
  text-align: left;
`;

const RightSide = styled.div`
  display: flex;
  flex-direction: row;
  width: 100%;
`;

const ExporePanel = styled.div`
  width: 80%;
`;

const Links = styled.div`
  display: flex;
  flex-direction: column;
  text-align: left;

  text-decoration: none;
`;

const RedirectLink = styled(Link)`
  text-decoration: none;
  color: white;
`;

const NewTabButton = styled.a`
  cursor: pointer;
`;

const BackToTop = styled.div`
  
  margin-right: 5rem;
  width: 100%;
  text-align: right;
  svg{
    font-size: 2rem;
  }
`;

function Footer() {
  const openLink = (url) => {
    const win = window.open(url, '_blank');
    if (win) {
      win.focus();
    }
  };

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <FooterContainer>
      <Content>
        <InfoPanel>
          <h1>Website Title</h1>
        </InfoPanel>
        <RightSide>
          <ExporePanel>
            <h3>Links</h3>
            <br />
            <Links>
              <RedirectLink to='/'>Home</RedirectLink>
              <RedirectLink to='/link1'>Link1</RedirectLink>
              <RedirectLink to='/link2'>Link2</RedirectLink>
              <RedirectLink to='/link3'>Link3</RedirectLink>
            </Links>
          </ExporePanel>
          {/* <BackToTop>
            <NewTabButton onClick={scrollToTop}>
              <FaArrowAltCircleUp />
            </NewTabButton>
          </BackToTop> */}
        </RightSide>
      </Content>
    </FooterContainer>
  );
}

export default Footer;
