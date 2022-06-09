----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    14:14:04 05/04/2022 
-- Design Name: 
-- Module Name:    fsm - Behavioral 
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
use IEEE.STD_LOGIC_UNSIGNED.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity fsm is
    Port ( CLK: in  STD_LOGIC;
           RESET: in  STD_LOGIC;
			  ROT_DONE: in std_logic;
			  DIR: out std_logic;
			  ROT: out std_logic;
			  ANIM: out std_logic);
end fsm;

architecture Behavioral of fsm is
--Insert the following in the architecture before the begin keyword
   --Use descriptive names for the states, like st1_reset, st2_search
   type state_type is (INIT, RIGHT3, LEFT3, ANIMATION); 
   signal state, next_state : state_type; 
   --Declare internal signals for all outputs of the state-machine
	signal start_cnt : std_logic_vector(23 downto 0):= (0 => '1', others => '0');
   --other outputs
begin
--Insert the following in the architecture after the begin keyword
   SYNC_PROC: process (clk)
   begin
      if rising_edge(clk) then
			start_cnt <= start_cnt + 1;
         if (reset = '1') then
            state <= INIT;
         else
            state <= next_state;
         -- assign other outputs to internal signals
         end if;        
      end if;
   end process;
 
   --MEALY State-Machine - Outputs based on state and inputs
   
 
   NEXT_STATE_DECODE: process (state)
   begin
      --declare default state for next_state to avoid latches
      next_state <= state;  --default is to stay in current state
      --insert statements to decode next_state
      --below is a simple example
      case (state) is
         when INIT =>
				dir <= '0';
				anim <= '0';
				rot <= '0';
            if start_cnt = 0 then
               next_state <= RIGHT3;
            end if;
         when RIGHT3 =>
				rot <= '1';
				dir <= '0';
				anim <= '0';
				if rot_done = '1' then
               next_state <= LEFT3;
					rot <= '0';
            end if;
         when LEFT3 =>
				rot <= '1';
				dir <= '1';
				anim <= '0';
				if rot_done = '1' then
               next_state <= ANIMATION;
					rot <= '0';
					anim <= '1';
					dir <= '0';
            end if;
         when ANIMATION =>
				rot <= '1';
				anim <= '1';
				dir <= '0';
				if rot_done = '1' then
               next_state <= INIT;
					rot<= '0';
            end if;
         when others =>
            next_state <= INIT;
      end case;   
   end process;


end Behavioral;

