require "fileinto";

if header :contains "X-Spam-Flag" "YES" {
  fileinto "Junk";
}
else {
  fileinto "Inbox";
}
