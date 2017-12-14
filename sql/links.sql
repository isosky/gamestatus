/*
Navicat PGSQL Data Transfer

Source Server         : localhost
Source Server Version : 90505
Source Host           : localhost:5432
Source Database       : fuyang
Source Schema         : public

Target Server Type    : PGSQL
Target Server Version : 90505
File Encoding         : 65001

Date: 2017-12-14 17:31:45
*/


-- ----------------------------
-- Table structure for links
-- ----------------------------
DROP TABLE IF EXISTS "public"."links";
CREATE TABLE "public"."links" (
"uuid" varchar(41) COLLATE "default",
"pt1_lon" numeric(20,8),
"pt1_lat" numeric(20,8),
"pt2_lon" numeric(20,8),
"pt2_lat" numeric(20,8),
"angle" numeric(20,8)
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of links
-- ----------------------------
INSERT INTO "public"."links" VALUES ('link-4bd76299-b064-42a3-8ed2-265c203d282f', '115.81977278', '32.88967579', '115.81957430', '32.89000012', '328.53423205');
INSERT INTO "public"."links" VALUES ('link-713f8601-90fb-4538-8d22-7f428b6a4726', '115.81955820', '32.88952376', '115.81977278', '32.88966678', '56.31549072');
INSERT INTO "public"."links" VALUES ('link-76b2fea1-1a9d-474e-8392-6f69857317c9', '115.81954747', '32.89000688', '115.81953675', '32.88952883', '181.28566823');
INSERT INTO "public"."links" VALUES ('link-83c1bca9-1bfd-430c-9dd4-e8fe91d16c59', '115.81977278', '32.88967579', '115.81929266', '32.88985260', '290.21651888');
INSERT INTO "public"."links" VALUES ('link-aee0b003-0fd1-48b8-acbe-1708e7a97a75', '115.81743658', '32.89017355', '115.81697255', '32.89025463', '279.91167318');
INSERT INTO "public"."links" VALUES ('link-b1595fbf-3571-465a-9ddc-5fb8d6f767b8', '115.81930071', '32.88981994', '115.81977278', '32.88966678', '107.97493670');
INSERT INTO "public"."links" VALUES ('link-b60b0434-598b-4d01-8d2f-6e13bda1a96f', '115.81696182', '32.89014540', '115.81713617', '32.89010485', '103.09069119');
INSERT INTO "public"."links" VALUES ('link-b60b0434-598b-4d01-8d2f-6e13bda1a96f', '115.81713617', '32.89010485', '115.81726223', '32.89004292', '116.16590254');
INSERT INTO "public"."links" VALUES ('link-b60b0434-598b-4d01-8d2f-6e13bda1a96f', '115.81726223', '32.89004292', '115.81735343', '32.88996409', '130.84053126');
INSERT INTO "public"."links" VALUES ('link-b60b0434-598b-4d01-8d2f-6e13bda1a96f', '115.81735343', '32.88996409', '115.81745535', '32.88984471', '139.50803859');
INSERT INTO "public"."links" VALUES ('link-d8368349-b13a-4922-a08e-8fd3ccf6c4e8', '115.81955820', '32.88952376', '115.81957430', '32.89000012', '1.93493044');
INSERT INTO "public"."links" VALUES ('link-dfcd8a44-5803-4884-a478-8db1cc3e990d', '115.81954747', '32.89000688', '115.81929266', '32.88985260', '238.80597700');
INSERT INTO "public"."links" VALUES ('link-e078dbb2-807e-4522-836b-0e690a87e40c', '115.81954747', '32.89000688', '115.81977278', '32.88966678', '146.47650293');
INSERT INTO "public"."links" VALUES ('link-e3b2c258-d109-4f43-850a-c0f451eb4ea3', '115.81977278', '32.88967579', '115.81953675', '32.88952883', '238.09228016');
INSERT INTO "public"."links" VALUES ('link-f14633c2-cd68-43a9-bda7-038a8d836dcf', '115.81955820', '32.88952376', '115.81929266', '32.88985260', '321.07870331');
INSERT INTO "public"."links" VALUES ('link-fad647da-e3da-4ae8-868e-8dc63e380490', '115.81930071', '32.88981994', '115.81957430', '32.89000012', '56.63108393');
INSERT INTO "public"."links" VALUES ('link-fb4fb21e-7f49-438f-aef8-54bf40a54068', '115.81690282', '32.89022310', '115.81738561', '32.89013976', '99.79319372');

-- ----------------------------
-- Alter Sequences Owned By 
-- ----------------------------
