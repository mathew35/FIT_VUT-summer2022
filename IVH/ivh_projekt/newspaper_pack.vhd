--------------------------------------------------------------------------------
-- Create Date:   21:45:06 03/11/2022
-- Author:			Matus Vrablik
-- login:			xvrabl05   
-- Module Name:   C:/FitkitSVN/apps/IVH/IVH_part_1/newspaper_pack.vhd
-- Project Name:  IVH_part_1
--------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.all;
package newspaper_pack is

	type DIRECTION_T is
		(DIR_LEFT,DIR_RIGHT);
		
	function GETCOLUMN ( signal DATA : in std_logic_vector; COLID : in integer; ROWS : in integer) return std_logic_vector;

end newspaper_pack;

package body newspaper_pack is

	function GETCOLUMN ( signal DATA : in std_logic_vector; COLID : in integer; ROWS : in integer)
		return std_logic_vector is
		
		begin
			return DATA(ROWS*COLID mod DATA'LENGTH to (ROWS*(COLID+1)-1) mod DATA'LENGTH);
		end GETCOLUMN;
 
end newspaper_pack;
