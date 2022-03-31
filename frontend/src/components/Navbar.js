import React, { useState } from 'react';
import { IconContext } from 'react-icons/lib';
import { Link } from 'react-router-dom';
import { FaTimes, FaBars } from 'react-icons/fa';
import styled from 'styled-components';

const NavBar = styled.div`
  height: 80px;

  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 999;

  margin: 0;
  padding: 0 50px;

  @media screen and (max-width: 960px) {
    position: sticky;
    top: 0;
  }
`;

const NavbarLogo = styled(Link)`
  text-decoration: none;
  color: black;
`;

const MenuIcon = styled.div`
  display: none;

  @media screen and (max-width: 960px) {
    display: block;
    font-size: 2rem;
  }
`;

const NavMenu = styled.ul`
  display: flex;
  padding: 0;
  margin: 0;

  @media screen and (min-width: 960px) {
    justify-content: center;
    align-items: center;
    list-style: none;
  }

  @media screen and (max-width: 960px) {
    flex-direction: column;
    position: absolute;
    background: black;
    height: calc(100vh - 85px);
    top: 80px;
    left: ${(props) => (props.active ? '0' : '-100%')};
    width: 100%;
    z-index: -1;
    transition: all 0.5s ease;
  }
`;

const NavItem = styled.li`
  color: black;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 2px solid transparent;
  @media screen and (max-width: 960px) {
    height: 100%;
    color: white;
    font-size: 2rem;
  }
`;

const NavLinks = styled(Link)`
  text-decoration: none;
  padding: 0 10px;
  height: 100%;
`;

function Navbar() {
  const [click, setClick] = useState(false);

  const handleClick = () => setClick(!click);
  const closeMobileMenu = () => setClick(false);

  return (
    <>
      <IconContext.Provider value={{ color: 'black' }}>
        <NavBar>
          <NavbarLogo to='/'>
            <h2>Website Title</h2>
          </NavbarLogo>

          <MenuIcon onClick={handleClick}>
            {click ? <FaTimes /> : <FaBars />}
          </MenuIcon>

          <NavMenu active={click}>
            <NavLinks to='/link1' onClick={closeMobileMenu}>
              <NavItem>Link1</NavItem>
            </NavLinks>
            <NavLinks to='/link2' onClick={closeMobileMenu}>
              <NavItem>Link2</NavItem>
            </NavLinks>
            <NavLinks to='/link3' onClick={closeMobileMenu}>
              <NavItem>Link3</NavItem>
            </NavLinks>
          </NavMenu>
        </NavBar>
      </IconContext.Provider>
    </>
  );
}

export default Navbar;
