-- Citac s volitelnou frekvenci
-- IVH projekt - ukol2
-- autor: ???

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
-- v pripade nutnosti muzete nacist dalsi knihovny

entity counter is
	 Generic (
			CLK_PERIOD : integer := 10 ;
			OUT_PERIOD : integer := 1000 );			
    Port ( CLK : in  STD_LOGIC;
           RESET : in  STD_LOGIC;
           EN : out  STD_LOGIC);
end counter;

architecture Behavioral of counter is

-- zde je funkce log2 z prednasek, pravdepodobne se vam bude hodit.
	function log2(A: integer) return integer is
		variable bits : integer := 0;
		variable b : integer := 1;
	begin
		while (b <= a) loop
			b := b * 2;
			bits := bits + 1;
		end loop;
		return bits;
	end function;
	
begin
	cnt :process(CLK,RESET)
	variable count : integer := 1;
	variable period : integer := OUT_PERIOD;
	begin
	if rising_edge(CLK) then
		if RESET = '1' then
			period := OUT_PERIOD;
			EN <= '0';
		else
			if period = 0 then
				period := OUT_PERIOD;
				EN <= '1';
				count := 1;
			else
				count := count - 1;
				if count = 0 then
					count := 1;
					EN <= '0';
				end if;
			end if;
			period := period - CLK_PERIOD;
		end if;
	end if;
	
	end process;
-- citac bude mit 2 genericke parametry: periodu hodinoveho signalu (CLK_PERIOD) a vystupni
-- periodu (OUT_PERIOD) (obe dve zadane jako cas). Citac s periodou odpovidajici OUT_PERIOD
-- (t.j., napr za 1 ms) aktivuje na jeden hodinovy cyklus signal EN po dobu jednoho taktu CLK
-- reset je aktivni v 1: tj kdyz je reset = 1, tak se vymaze vnitrni citac
-- pro zjednoduseni pocitejte, ze OUT_PERIOD je delitelne CLK_PERIOD beze zbytku a je vetsi.

-- Signal EN bude aktivovany po 1 periodu hodinoveho vstupu CLK - k cemu vam staci pouze 
-- signal CLK a jeho priznak CLK'event. Genericke parametry OUT_PERIOD a CLK_FPERIOD slouzi pouze 
-- k vypoctu toho,  do kolika citac pocita. 

end Behavioral;