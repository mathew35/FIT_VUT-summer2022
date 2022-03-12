--------------------------------------------------------------------------------
-- Create Date:   21:43:14 03/11/2022
-- Author:			Matus Vrablik
-- login:			xvrabl05   
-- Module Name:   C:/FitkitSVN/apps/IVH/IVH_part_1/newspaper_pack_tb.vhd
-- Project Name:  IVH_part_1
--------------------------------------------------------------------------------
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE work.newspaper_pack.ALL;

 
ENTITY newspaper_pack_tb IS
END newspaper_pack_tb;
 
ARCHITECTURE behavior OF newspaper_pack_tb IS 

   signal DATA : std_logic_vector(0 to 11) := (others => '0');
 
BEGIN
	process
	begin
		DATA <= "101001100111";
		wait for 10 ns;
		
		assert GETCOLUMN(DATA,0,3) /= "101" report "Pass 0,3 = 101" severity note;
		assert GETCOLUMN(DATA,1,3) /= "001" report "Pass 1,3 = 001" severity note;
		assert GETCOLUMN(DATA,4,3) /= "101" report "Pass 4,3 = 101" severity note;
		assert GETCOLUMN(DATA,-1,3) /= "111" report "Pass -1,3 = 111" severity note;
		assert GETCOLUMN(DATA,-1,4) /= "0111" report "Pass -1,4 = 0111" severity note;
		assert GETCOLUMN(DATA,-3,4) /= "1010" report "Pass -1,4 = 1010" severity note;

		wait;
	end process;

END;