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

Date: 2017-12-14 17:31:38
*/


-- ----------------------------
-- Table structure for segments
-- ----------------------------
DROP TABLE IF EXISTS "public"."segments";
CREATE TABLE "public"."segments" (
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
-- Records of segments
-- ----------------------------
INSERT INTO "public"."segments" VALUES ('lane-1203e89b-26d8-4151-8bd5-4f8f8d3338cf', '115.81953675', '32.89153392', '115.81954479', '32.89094157', '179.22171991');
INSERT INTO "public"."segments" VALUES ('lane-3cf05857-878c-4443-9568-ef29d7dd1985', '115.81738561', '32.89013976', '115.81836261', '32.88995733', '100.57709797');
INSERT INTO "public"."segments" VALUES ('lane-40e9fc21-c254-4db8-bbb2-b85e83e1ed64', '115.81638783', '32.89031432', '115.81690282', '32.89022310', '100.04443665');
INSERT INTO "public"."segments" VALUES ('lane-44846a26-fcf3-41cf-9126-fccd3da80402', '115.81929266', '32.88985260', '115.81854936', '32.88999196', '280.61894658');
INSERT INTO "public"."segments" VALUES ('lane-4d569435-9ebf-4853-b198-d5e34db75cf8', '115.81745535', '32.88984471', '115.81918001', '32.88793024', '137.98573588');
INSERT INTO "public"."segments" VALUES ('lane-65d07ba1-b318-409f-929a-7ca37ac2705c', '115.81854567', '32.88995846', '115.81743658', '32.89017355', '280.97548825');
INSERT INTO "public"."segments" VALUES ('lane-6e27249f-7501-4c01-8e28-0a01d99b062a', '115.81954479', '32.89094157', '115.81954747', '32.89000688', '179.83558461');
INSERT INTO "public"."segments" VALUES ('lane-7a4c9c58-d659-43a0-836a-073ec2dd62d2', '115.81977278', '32.88966678', '115.82137138', '32.88895055', '114.13424857');
INSERT INTO "public"."segments" VALUES ('lane-7c939253-e670-4c2e-8342-29f08ebece8c', '115.81956893', '32.88861495', '115.81955820', '32.88952376', '359.32363243');
INSERT INTO "public"."segments" VALUES ('lane-7f90b68e-8b1e-4fb9-adf8-0baeeef560d8', '115.81957430', '32.89000012', '115.81956357', '32.89152941', '359.59804494');
INSERT INTO "public"."segments" VALUES ('lane-8500a9af-18c5-4d92-8e8c-9a6004d9f26e', '115.81697255', '32.89025463', '115.81640124', '32.89036049', '280.49720040');
INSERT INTO "public"."segments" VALUES ('lane-913da18b-1214-45c9-b438-12d42b0c9817', '115.81836730', '32.88999111', '115.81930071', '32.88981994', '100.39178583');
INSERT INTO "public"."segments" VALUES ('lane-b24bdddb-2f65-459f-9470-fb105017df1a', '115.82137942', '32.88896519', '115.82065657', '32.88928840', '294.09062164');
INSERT INTO "public"."segments" VALUES ('lane-d68d8eb1-e9ab-4743-84a8-c4003687c366', '115.81953809', '32.88952827', '115.81955016', '32.88813295', '179.50438377');
INSERT INTO "public"."segments" VALUES ('lane-da4b1152-4639-4947-8fd7-8321db1f0ac6', '115.82065657', '32.88928840', '115.81977278', '32.88967579', '293.66957710');
INSERT INTO "public"."segments" VALUES ('lane-f1865a0e-a15f-4a11-bf85-289615bdfe47', '115.81957966', '32.88813295', '115.81956893', '32.88861495', '358.72486199');

-- ----------------------------
-- Alter Sequences Owned By 
-- ----------------------------
