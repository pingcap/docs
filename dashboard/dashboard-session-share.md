---
title: Share TiDB Dashboard Sessions
summary: Learn how to share current TiDB Dashboard sessions to others to access.
---

# Share TiDB Dashboard Sessions

You can share the current session of the TiDB Dashboard to other users so that they can access and operate the TiDB Dashboard without entering the user password.

## Steps for the Inviter

1. Sign into TiDB Dashboard.

2. Click the username in the left sidebar to access the configure page.

3. Click **Share Current Session**.

   ![Sample Step](/media/dashboard/dashboard-session-share-settings-1.png)

   > **Note:**
   >
   > For security, the shared session cannot be shared again.

4. Adjust sharing settings in the popup dialog:

   - Expire in: How long the shared session will last for. Signing out the current session will not sign out any shared sessions.

   - Share as read-only privilege: The shared session can only perform read operations but not write operations (like modifying configurations).

5. Click **Generate Authorization Code**.

   ![Sample Step](/media/dashboard/dashboard-session-share-settings-2.png)

6. Provide the generate **Authorization Code** to the user that you want to share session to.

   ![Sample Step](/media/dashboard/dashboard-session-share-settings-3.png)

   > **Warning:**
   >
   > Anyone can use the TiDB Dashboard with the authorization code. For this reason, please keep the authorization code secure and do not send it to someone that is untrusted to avoid unauthorized access.

## Steps for the Invitee

1. In the sign in page in TiDB Dashboard, click **Use Alternative Authentication**.

   ![Sample Step](/media/dashboard/dashboard-session-share-signin-1.png)

2. Click **Authorization Code** to use it to sign in.

   ![Sample Step](/media/dashboard/dashboard-session-share-signin-2.png)

3. Enter the authorization code you receive from others.

4. Click **Sign In**.

   ![Sample Step](/media/dashboard/dashboard-session-share-signin-3.png)
