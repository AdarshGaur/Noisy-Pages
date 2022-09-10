export const LoginStart = (userCredentials) => ({
	type: "LOGIN_START",
});

export const LoginSuccess = (user) => ({
	type: "LOGIN_SUCCESS",
	payload: user,
});

export const LoginFailure = () => ({
	type: "LOGIN_FAILURE",
});

export const Logout = () => ({
	type: "LOGOUT",
});

export const UpdateStarte = (userCredentials) => ({
	type: "UPDATE_START",
});


export const UpdateSuccess = (userCredentials) => ({
	type: "UPDATE_SUCCESS",
	payload: user,
});

export const UpdateFailure = (userCredentials) => ({
	type: "UPDATE_FAILURE",
});

