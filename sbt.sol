// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts@4.7.2/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts@4.7.2/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts@4.7.2/access/Ownable.sol";
import "@openzeppelin/contracts@4.7.2/utils/Counters.sol";

contract SoulBoundVaccine is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;
    event Attest(address indexed to, uint256 indexed tokenId);
    event Revoke(address indexed to, uint256 indexed tokenId);

    mapping(uint256 => string) private _title;
    mapping(address => uint256[]) certificates;
    constructor() ERC721("SoulBoundVaccine", "SBV") {}


    // Function to emit and assign a new SBT
    // The safeMint function is used to issue (and thus assign) a Soulbound Token,
    // which takes the address to which the token should be delivered as well as
    // other accessory data (i.e. the URI of a remote resource).


    function safeMint(address to, string memory uri, string memory _vaccine) public onlyOwner {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
        _title[tokenId] = _vaccine;
        certificates[to].push(tokenId);
    }



    // The following two functions are the overriding of inherited functions to satisfy the requirement of
    // non-transferability and the issuance and revocation of tokens by the creator (or owner) of the smart contract.
    // To fo this, specific constraints for transferring, attestation, and revocation must be added to the
    // ERC721 token.

    // beforeTokenTransfer funtion has been overridden to provide the checks to prevent token transferring


    function _beforeTokenTransfer(address from,  address to, uint256 tokenId) internal override virtual {
        require( from == address(0) || to == address(0), "You are not authorized to transfer the token.");
    }

    // afterTokenTransfer function has been overridden to implement the events attestation and revocation.

    function _afterTokenTransfer(address from, address to, uint256 tokenId) internal override virtual {
            if(from == address(0)){
                emit Attest(to, tokenId);
            }
            else if (to == address(0)){
                emit Revoke(to, tokenId);
            }
    }


    // overriding of burn
    function burn(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Only token owner can burn it");
        _burn(tokenId);
    }

    // revoke (Burning)
    function revoke(uint256 tokenId, address owner) onlyOwner external {
        require(balanceOf(owner) != 0, "ERC721: balance of is 0");
        _burn(tokenId);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }


    // Reding Title
    function titleOf(uint256 tokenId) public view virtual returns (string memory) {
        return _title[tokenId];
    }

    // Reading URI
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function getCertificates(address address_to) public view returns(uint256[] memory){

        return certificates[address_to];
    }
}