--------------------------------------------------------------------------------
-- Create Date:   12:45:23 05/03/2022
-- Author:			Matus Vrablik
-- login:			xvrabl05   
-- Module Name:   C:/FitkitSVN/apps/IVH/display/column.vhd
-- Project Name:  display
--------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

use work.newspaper_pack.all;

entity column is
    Port ( CLK : in  STD_LOGIC;
           RESET : in  STD_LOGIC;
           STATE : out  STD_LOGIC_VECTOR;
           INIT_STATE : in  STD_LOGIC_VECTOR;
           NEIGH_LEFT : in  STD_LOGIC_VECTOR;
           NEIGH_RIGHT : in  STD_LOGIC_VECTOR;
           DIRECTION : in  DIRECTION_T;
           EN : in  STD_LOGIC);
end column;

architecture Behavioral of column is
begin
	process (clk,reset,en) is
	variable state_changed: std_logic := '0';
	begin
		if rising_edge(clk) then
			if reset = '1' then
				STATE <= INIT_STATE;
				state_changed := '0';
			end if;
			if state_changed = '0' then
				STATE <= INIT_STATE;
			end if;
			if EN = '1' then
				state_changed := '1';
				if DIRECTION = DIR_RIGHT then
					STATE <= NEIGH_RIGHT;
				else
					STATE <= NEIGH_LEFT;
				end if;
			end if;
		end if;
	end process;
end Behavioral;

