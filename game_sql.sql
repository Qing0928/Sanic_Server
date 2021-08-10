-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2021-08-10 09:32:26
-- 伺服器版本： 10.4.20-MariaDB
-- PHP 版本： 8.0.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫: `game_sql`
--

-- --------------------------------------------------------

--
-- 資料表結構 `action_230417`
--

CREATE TABLE `action_230417` (
  `account` varchar(40) NOT NULL,
  `action` varchar(40) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 傾印資料表的資料 `action_230417`
--

INSERT INTO `action_230417` (`account`, `action`) VALUES
('test05', 'item_3'),
('test08', ''),
('test09', ''),
('test10', '');

-- --------------------------------------------------------

--
-- 資料表結構 `reward`
--

CREATE TABLE `reward` (
  `account` varchar(40) NOT NULL DEFAULT '',
  `team_id` int(11) DEFAULT 0,
  `data` varchar(500) DEFAULT '',
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 傾印資料表的資料 `reward`
--

INSERT INTO `reward` (`account`, `team_id`, `data`, `time`) VALUES
('test07', 450698, 'item_1:1, item_3:2, skill_u_1:1', '2021-07-29 00:00:00');

-- --------------------------------------------------------

--
-- 資料表結構 `status_230417`
--

CREATE TABLE `status_230417` (
  `account` varchar(40) NOT NULL,
  `enhance_sk1` int(11) NOT NULL DEFAULT 0,
  `enhance_sk2` int(11) NOT NULL DEFAULT 0,
  `enhance_sk3` int(11) NOT NULL DEFAULT 0,
  `enhance_sk4` int(11) NOT NULL DEFAULT 0,
  `enhance_de1` int(11) NOT NULL DEFAULT 0,
  `enhance_de2` int(11) NOT NULL DEFAULT 0,
  `enhance_de3` int(11) NOT NULL DEFAULT 0,
  `gather` int(11) NOT NULL DEFAULT 0,
  `immortal` int(11) NOT NULL DEFAULT 0,
  `numb` int(11) NOT NULL DEFAULT 0,
  `sleep` int(11) NOT NULL DEFAULT 0,
  `poison` int(11) NOT NULL DEFAULT 0,
  `blood` int(11) NOT NULL DEFAULT 0,
  `drop_de1` int(11) NOT NULL DEFAULT 0,
  `drop_de2` int(11) NOT NULL DEFAULT 0,
  `drop_sk1` int(11) NOT NULL DEFAULT 0,
  `drop_sk2` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 傾印資料表的資料 `status_230417`
--

INSERT INTO `status_230417` (`account`, `enhance_sk1`, `enhance_sk2`, `enhance_sk3`, `enhance_sk4`, `enhance_de1`, `enhance_de2`, `enhance_de3`, `gather`, `immortal`, `numb`, `sleep`, `poison`, `blood`, `drop_de1`, `drop_de2`, `drop_sk1`, `drop_sk2`) VALUES
('boss', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
('test05', 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0),
('test08', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
('test09', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
('test10', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- 資料表結構 `teams`
--

CREATE TABLE `teams` (
  `leader` varchar(40) NOT NULL DEFAULT '',
  `member1` varchar(40) NOT NULL DEFAULT '',
  `member2` varchar(40) NOT NULL DEFAULT '',
  `member3` varchar(40) NOT NULL DEFAULT '',
  `id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 傾印資料表的資料 `teams`
--

INSERT INTO `teams` (`leader`, `member1`, `member2`, `member3`, `id`) VALUES
('test01', 'test07', 'test03', 'test02', 450698),
('test05', 'test08', 'test09', 'test10', 230417);

-- --------------------------------------------------------

--
-- 資料表結構 `user_info`
--

CREATE TABLE `user_info` (
  `account` varchar(40) NOT NULL,
  `password` varchar(40) NOT NULL,
  `name` varchar(40) NOT NULL,
  `play_status` int(11) DEFAULT 0,
  `team_id` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 傾印資料表的資料 `user_info`
--

INSERT INTO `user_info` (`account`, `password`, `name`, `play_status`, `team_id`) VALUES
('test01', '2c2bd10fa1418d6785ec3fbd181d4e', 'hashuser', 1, 450698),
('test02', 'b1de56a928d9c540050029866264a8', 'ouO', 1, 450698),
('test03', 'd421c9596d3bee15cd88b473d669c1', '=3=', 1, 450698),
('test05', 'bfd74bf3bf4c0ec87d51bad3234fcc', 'Ouo', 1, 230417),
('test07', 'b1de56a928d9c540050029866264a8', '=w=', 0, 450698);

-- --------------------------------------------------------

--
-- 資料表結構 `user_item`
--

CREATE TABLE `user_item` (
  `account` varchar(40) NOT NULL,
  `item_1` int(11) NOT NULL DEFAULT 0,
  `item_2` int(11) NOT NULL DEFAULT 0,
  `item_3` int(11) NOT NULL DEFAULT 0,
  `item_4` int(11) NOT NULL DEFAULT 0,
  `item_5` int(11) NOT NULL DEFAULT 0,
  `item_6` int(11) NOT NULL DEFAULT 0,
  `item_7` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 傾印資料表的資料 `user_item`
--

INSERT INTO `user_item` (`account`, `item_1`, `item_2`, `item_3`, `item_4`, `item_5`, `item_6`, `item_7`) VALUES
('test01', 0, 0, 0, 0, 0, 0, 0),
('test02', 0, 0, 0, 0, 0, 0, 0),
('test03', 0, 0, 0, 0, 0, 0, 0),
('test05', 0, 0, 1, 0, 0, 0, 0),
('test07', 0, 0, 0, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- 資料表結構 `user_skill`
--

CREATE TABLE `user_skill` (
  `account` varchar(40) NOT NULL,
  `skill_1` int(11) NOT NULL DEFAULT 1,
  `skill_2` int(11) NOT NULL DEFAULT 1,
  `skill_3` int(11) NOT NULL DEFAULT 0,
  `skill_4` int(11) NOT NULL DEFAULT 0,
  `skill_u_1` int(11) NOT NULL DEFAULT 0,
  `skill_u_2` int(11) NOT NULL DEFAULT 0,
  `career` varchar(40) NOT NULL DEFAULT 'x'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 傾印資料表的資料 `user_skill`
--

INSERT INTO `user_skill` (`account`, `skill_1`, `skill_2`, `skill_3`, `skill_4`, `skill_u_1`, `skill_u_2`, `career`) VALUES
('test01', 1, 1, 0, 0, 0, 0, 'x'),
('test02', 1, 1, 0, 0, 0, 0, 'x'),
('test03', 1, 1, 0, 0, 0, 0, 'x'),
('test05', 1, 1, 0, 0, 0, 0, 'fighter'),
('test07', 1, 1, 0, 0, 0, 0, 'x');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `action_230417`
--
ALTER TABLE `action_230417`
  ADD PRIMARY KEY (`account`);

--
-- 資料表索引 `reward`
--
ALTER TABLE `reward`
  ADD PRIMARY KEY (`time`);

--
-- 資料表索引 `status_230417`
--
ALTER TABLE `status_230417`
  ADD PRIMARY KEY (`account`);

--
-- 資料表索引 `teams`
--
ALTER TABLE `teams`
  ADD PRIMARY KEY (`leader`);

--
-- 資料表索引 `user_info`
--
ALTER TABLE `user_info`
  ADD PRIMARY KEY (`account`);

--
-- 資料表索引 `user_item`
--
ALTER TABLE `user_item`
  ADD PRIMARY KEY (`account`);

--
-- 資料表索引 `user_skill`
--
ALTER TABLE `user_skill`
  ADD PRIMARY KEY (`account`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
