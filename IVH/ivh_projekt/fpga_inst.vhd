library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.numeric_std.all;

use work.newspaper_pack.all;

architecture Behavioral of tlv_gp_ifc is
	signal A : std_logic_vector(3 downto 0) := "0000";
	signal R : std_logic_vector(7 downto 0) := (others => '0');
	
	signal cnt : std_logic_vector(12 downto 0) := (others => '0');  -- 60fps - log2(20MHz/(60*16)) ~ 14b --> 13b (bit faster to render flickering) 
	signal cnt_column : std_logic_vector(21 downto 0) := (21 downto 1 => '0',0 => '1');  -- 38 columns per second - log2(20MHz/(60*16)) ~ 14b --> 13b (bit faster to render flickering) 
	signal EN : std_logic := '0';
	
	signal rot_cnt: std_logic_vector(3 downto 0) := "0000";
	signal mov_cnt: std_logic_vector(3 downto 0) := "0000";
	signal rot: std_logic_vector(1 downto 0) := "00";
	signal rot_en: std_logic := '0';
	signal rot_confirm: std_logic := '0';
	signal animation: std_logic := '0';
	signal dir: std_logic := '0';
	
	type col_type is array (integer range 15 downto 0) of std_logic_vector(7 downto 0);
	signal COL: col_type :=(others => (others => '0'));
	signal COLa: col_type :=(others => (others => '0'));
	
	signal direction : DIRECTION_T := DIR_LEFT;
	signal data : std_logic_vector(127 downto 0):= (others => '0');
	signal dataanim : std_logic_vector(127 downto 0):= (others => '0');
	
	component column is
		port(
			CLK,RESET,EN : in std_logic;
			DIRECTION : DIRECTION_T;
			INIT_STATE, NEIGH_LEFT, NEIGH_RIGHT: in std_logic_vector;
			STATE : out std_logic_vector);
	end component;
	
	component rom is
		port(
			DATAANIM : out std_logic_vector;
			DATA : out std_logic_vector);
	end component;
	
	component fsm is
		port(
			CLK,RESET: in std_logic;
			ROT_DONE: in std_logic;
			DIR,ROT,ANIM: out std_logic);
	end component;
	
begin
	
	FSMm: fsm
		port map(clk,reset,rot_confirm,dir,rot_en,animation);
	
	rom16x8: rom
		port map(
		DATAANIM => dataanim,
		DATA => data);
		
	gen_cols:
	for i in 15 downto 0 generate
		COLX: column port map(clk,reset,EN,direction,DATA(7+i*8 downto i*8),COL(conv_integer(std_logic_vector(to_unsigned(i,4)+1))),COL(conv_integer(std_logic_vector(to_unsigned(i,4)-1))),COL(i)); 
		COLanim: column port map(clk,reset,EN,direction,DATAanim(7+i*8 downto i*8),COLa(conv_integer(std_logic_vector(to_unsigned(i,4)+1))),COLa(conv_integer(std_logic_vector(to_unsigned(i,4)-1))),COLa(i)); 
	end generate;
	
	process (clk) is
	begin
		if rising_edge(clk) then
			if dir = '0' then
				direction <= DIR_RIGHT;
			else
				direction <= DIR_LEFT;
			end if;
			cnt <= cnt + 1;
			EN <= '0';
			if conv_integer(cnt) = 0 then
				A <= A + 1;
				if animation = '1' then
					R <= COLA(conv_integer(A));
				else
					R <= COL(conv_integer(A));
				end if;
			end if;
			rot_confirm <= '0';
			if rot_en = '1' then
				cnt_column <= cnt_column + 1;
				if conv_integer(cnt_column) = 0 then
					EN <= '1';
					mov_cnt <= mov_cnt + 1;
					if mov_cnt <= "1111" then
						rot_cnt <= rot_cnt + 1;
					end if;
					if rot_cnt = "1111" then
						rot <= rot + 1;
					end if;
					if rot = "11" then
						rot_confirm <= '1';
						rot <= "00";
					end if;
				end if;
			end if;
		end if;
	
	end process;
	

    -- mapovani vystupu
    -- nemenit
    X(6) <= A(3);
    X(8) <= A(1);
    X(10) <= A(0);
    X(7) <= '0'; -- en_n
    X(9) <= A(2);
    X(16) <= R(1);
    X(18) <= R(0);
    X(20) <= R(7);
    X(22) <= R(2);
  
    X(17) <= R(4);
    X(19) <= R(3);
    X(21) <= R(6);
    X(23) <= R(5);
end Behavioral;

