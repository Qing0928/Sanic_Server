-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- 主機： localhost:3306
-- 產生時間： 2021 年 10 月 12 日 12:37
-- 伺服器版本： 8.0.26-0ubuntu0.20.04.3
-- PHP 版本： 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `game_sql`
--

-- --------------------------------------------------------

--
-- 資料表結構 `reward`
--

CREATE TABLE `reward` (
  `account` varchar(40) NOT NULL DEFAULT '',
  `team_id` int DEFAULT '0',
  `data` varchar(500) DEFAULT '',
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- 資料表結構 `teams`
--

CREATE TABLE `teams` (
  `leader` varchar(40) NOT NULL DEFAULT '',
  `member1` varchar(40) NOT NULL DEFAULT '',
  `member2` varchar(40) NOT NULL DEFAULT '',
  `member3` varchar(40) NOT NULL DEFAULT '',
  `id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- 傾印資料表的資料 `teams`
--

INSERT INTO `teams` (`leader`, `member1`, `member2`, `member3`, `id`) VALUES
('test05', 'test02', 'test03', 'test07', 230417);

-- --------------------------------------------------------

--
-- 資料表結構 `user_info`
--

CREATE TABLE `user_info` (
  `account` varchar(40) NOT NULL,
  `password` varchar(40) NOT NULL,
  `name` varchar(40) NOT NULL,
  `play_status` int DEFAULT '0',
  `team_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- 傾印資料表的資料 `user_info`
--

INSERT INTO `user_info` (`account`, `password`, `name`, `play_status`, `team_id`) VALUES
('a1', '8a8bb7cd343aa2ad99b7d762030857', 'a1', 1, 887671),
('a2', '693a9fdd4c2fd0700968fba0d07ff3', 'a2', 1, 887671),
('a3', '9d607a663f3e9b0a90c3c8d4426640', 'a3', 0, 328473),
('a4', '894f782a148b33af1e39a0efed952d', 'a4', 0, 954126),
('p1', 'ec6ef230f1828039ee794566b9c58a', 'pat', 0, 177918),
('saber0928', '81dc9bdb52d04dc20036dbd8313ed0', '炭烤A5和牛', 0, 741095),
('test02', 'b1de56a928d9c540050029866264a8', 'ouO', 0, 230417),
('test03', 'd421c9596d3bee15cd88b473d669c1', '=3=', 0, 230417),
('test05', 'bfd74bf3bf4c0ec87d51bad3234fcc', 'Ouo', 0, 230417),
('test07', 'b1de56a928d9c540050029866264a8', '=w=', 0, 230417);

-- --------------------------------------------------------

--
-- 資料表結構 `user_item`
--

CREATE TABLE `user_item` (
  `account` varchar(40) NOT NULL,
  `item_1` int NOT NULL DEFAULT '0',
  `item_2` int NOT NULL DEFAULT '0',
  `item_3` int NOT NULL DEFAULT '0',
  `item_4` int NOT NULL DEFAULT '0',
  `item_5` int NOT NULL DEFAULT '0',
  `item_6` int NOT NULL DEFAULT '0',
  `item_7` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- 傾印資料表的資料 `user_item`
--

INSERT INTO `user_item` (`account`, `item_1`, `item_2`, `item_3`, `item_4`, `item_5`, `item_6`, `item_7`) VALUES
('a1', 14, 15, 17, 20, 20, 4, 3),
('a2', 2, 0, 1, 3, 2, 3, 3),
('a3', 0, 0, 0, 0, 0, 0, 0),
('a4', 0, 0, 0, 0, 0, 0, 0),
('p1', 0, 0, 0, 0, 0, 0, 0),
('saber0928', 0, 0, 0, 0, 0, 0, 0),
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
  `skill_1` int NOT NULL DEFAULT '1',
  `skill_2` int NOT NULL DEFAULT '1',
  `skill_3` int NOT NULL DEFAULT '0',
  `skill_4` int NOT NULL DEFAULT '0',
  `skill_u_1` int NOT NULL DEFAULT '0',
  `skill_u_2` int NOT NULL DEFAULT '0',
  `career` varchar(40) NOT NULL DEFAULT 'x'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- 傾印資料表的資料 `user_skill`
--

INSERT INTO `user_skill` (`account`, `skill_1`, `skill_2`, `skill_3`, `skill_4`, `skill_u_1`, `skill_u_2`, `career`) VALUES
('a1', 1, 1, 1, 1, 1, 1, 'traveler'),
('a2', 1, 1, 1, 1, 1, 1, 'magician'),
('a3', 1, 1, 1, 1, 1, 1, 'fighter'),
('a4', 1, 1, 1, 1, 1, 1, 'assistant'),
('p1', 1, 1, 0, 0, 0, 0, 'assistant'),
('saber0928', 1, 1, 1, 1, 1, 1, 'fighter'),
('test02', 1, 1, 0, 0, 0, 0, 'traveler'),
('test03', 1, 1, 0, 0, 0, 0, 'magician'),
('test05', 1, 1, 0, 0, 0, 0, 'fighter'),
('test07', 1, 1, 0, 0, 0, 0, 'assistant');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `reward`
--
ALTER TABLE `reward`
  ADD PRIMARY KEY (`time`);

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
