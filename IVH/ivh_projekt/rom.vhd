----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    18:44:15 05/04/2022 
-- Design Name: 
-- Module Name:    rom - Behavioral 
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
-- Description: 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: 
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

use work.newspaper_pack.GETCOLUMN;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity rom is
    Port ( DATAanim : out std_logic_vector(127 downto 0);
			  DATA : out  STD_LOGIC_VECTOR(127 downto 0));
end rom;

architecture rtl of rom is
constant rom: std_logic_vector(127 downto 0) := ("00000000"&
									 "00000000"&
									 "01111110"&
									 "00001000"&
									 "01111110"&
									 "00000000"&
									 "00011110"&
									 "01100000"&
									 "00011110"&
									 "00000000"&
									 "01111110"&
									 "00000000"&
									 "00000000"&
									 "00111110"&
									 "00000011"&
									 "00100010");
constant romA: std_logic_vector(127 downto 0) := ("00000001"&
									 "00000010"&
									 "00000100"&
									 "00001000"&
									 "00010000"&
									 "00100000"&
									 "01000000"&
									 "10000000"&
									 "10000000"&
									 "01000000"&
									 "00100000"&
									 "00010000"&
									 "00001000"&
									 "00000100"&
									 "00000010"&
									 "00100001");
begin
	DATA <= rom;
	DATAanim <= romA;
end architecture;