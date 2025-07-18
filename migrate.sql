CREATE TABLE vouchers (
	user_id VARCHAR NOT NULL, 
	voucher_url VARCHAR NOT NULL, 
	PRIMARY KEY (user_id)
);
INSERT INTO vouchers VALUES('12345','https://eyeqcoach.com/activation?code=18724528-4e77-4e6f-81a0-7f8f816f233a');
INSERT INTO vouchers VALUES('67890','https://eyeqcoach.com/activation?code=18724528-4e77-4e6f-81a0-7f8f816f233a');
COMMIT;
